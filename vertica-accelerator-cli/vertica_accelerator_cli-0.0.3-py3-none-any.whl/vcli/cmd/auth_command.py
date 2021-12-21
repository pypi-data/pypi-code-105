#!/bin/python3
# coding=utf-8
# ------------------------------------------------------------------------------
# Created on October 05 12:49 2021
#
# Vertica Vaas Okta Login command
#
# Usage:
#   va login
#   va login --profile profile2
#
# (c) Copyright 2021 Micro Focus or one of its affiliates.
# ------------------------------------------------------------------------------
import pkce
import requests
import uuid
import json
import secrets
import re
from argparse import Namespace
from vcli.cmd.sub_command import SubCommandImplementation
from vcli.constant import VCLI_CONFIG_DEFAULT, REDIRECT_URL_CONSTANT
from vcli.models.vcli_config_file import VcliConfigFile
from vcli.models.vcli_credential_file import VcliCredentialFile
from vcli.exceptions.vcli_custom_exception import AccessTokenFailedError, ProfileNotExistError
from vcli.util.vcli_logger import logger
from vcli.util.error_message import ErrorMessage
from vcli.cmd.config_command import ConfigCommand
from vcli.util.help_message import HelpMessage
from vcli.util.utils import build_api_client, verify_access_token
from openapi_client.exceptions import ServiceException
from openapi_client.api.index_v1_api import IndexV1Api


class AuthCommand(SubCommandImplementation):
    def operation_define(self, subparsers) -> None:
        # Supported command line options:
        #   va login
        #   va login --profile profile2
        login_parser = subparsers.add_parser('login', help=HelpMessage.login_header)
        login_parser.add_argument('--profile', default=VCLI_CONFIG_DEFAULT, metavar='<value>', type=str, help=HelpMessage.profile)
        login_parser.set_defaults(func=self.operation_cmd)

        logout_parser = subparsers.add_parser('logout', help=HelpMessage.logout_header)
        logout_parser.add_argument('--profile', default=VCLI_CONFIG_DEFAULT, metavar='<value>', type=str, help=HelpMessage.profile)
        logout_parser.set_defaults(func=self.operation_logout)

    def operation_cmd(self, args: Namespace) -> None:
        try:
            VcliConfigFile.check_profile_file(profile=args.profile)
            VcliCredentialFile.check_profile_file(profile=args.profile)
        except ProfileNotExistError:
            logger.info("profile file not found")
            vcli_config_data, vcli_credential_data = ConfigCommand.read_user_input_all(args=args)
            ConfigCommand.set_config_data(
                vcli_config_data=vcli_config_data,
                vcli_credential_data=vcli_credential_data,
                profile=args.profile
            )

        config_file = VcliConfigFile.read_profile_config(profile=args.profile)
        credential_file = VcliCredentialFile.read_profile_config(profile=args.profile)

        # Step 1: Get the session token, code challenge and code verifier
        session_token, code_challenge, code_verifier = self.__create_auth_session(config_file=config_file, credential_file=credential_file)
        # Step 2: Get access code
        auth_code = self.__get_auth_code(
            config_file=config_file,
            credential_file=credential_file,
            code_challenge=code_challenge,
            session_token=session_token
        )
        # Step 3: Get access token
        access_token = self._get_access_token(
            config_file=config_file,
            credential_file=credential_file,
            auth_code=auth_code,
            code_verifier=code_verifier
        )
        # Step 4: Verify the access token and stored it in credentials config
        verify_access_token(
            credential_file=credential_file,
            access_token=access_token,
            profile=args.profile
        )
        # Step 5. hit health of oa
        # TODO: DISABLE THIS FOR NOW
        # self._valid_oa_health(args=args)
        # TODO: After login, save oa version into config file. Apply version support or not.
        print("Login success")

    def operation_logout(self, args: Namespace) -> None:
        credential_file = VcliCredentialFile.read_profile_config(profile=args.profile)
        credential_file.delete_access_token(profile=args.profile)
        print("Logout success")

    def _valid_oa_health(self, args: Namespace):
        """Check if remote oa is in health condition.

        Args:
            args (Namespace): args passed down from cmd
        """
        api_client = build_api_client(profile=args.profile)
        try:
            IndexV1Api(api_client=api_client).services_health_get()
        except ServiceException as se:
            logger.debug(se)
            print("WARNING: OA Service health check did not pass")
        except Exception as e:
            logger.debug(e)
            print("WARNING: Failed to check OA Service health")

    def __create_auth_session(self, config_file: VcliConfigFile, credential_file: VcliCredentialFile) -> [str, str, str]:
        """create auth session and prepare to send to okta for authentication

        Args:
            config_file (VcliConfigFile): config file content.
            credential_file (VcliCredentialFile): credential file content.

        Raises:
            AccessTokenFailedError: Raised when user name or passwd is wrong

        Returns:
            [str, str, str]: session_token, code_challenge, code_verifier
        """
        okta_url = credential_file.auth_endpont
        username = credential_file.username
        password = credential_file.password
        code_verifier, code_challenge = pkce.generate_pkce_pair()
        response = requests.post(
            url=f"{okta_url}/api/v1/authn",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            data=json.dumps(
                {
                    "username": username,
                    "password": password,
                    "options": {
                        "multiOptionalFactorEnroll": True,
                        "warnBeforePasswordExpired": True,
                    },
                }
            )
        )
        result = response.json()
        session_token = result.get('sessionToken')
        if not session_token:
            raise AccessTokenFailedError(ErrorMessage.LOGIN_FAILED_BAD_USERNAME_OR_PASSWORD)
        result.pop('sessionToken', None)
        logger.debug(f"create auth session step: {result}")
        return session_token, code_challenge, code_verifier

    def __get_auth_code(
        self,
        config_file: VcliConfigFile,
        credential_file: VcliCredentialFile,
        code_challenge: str,
        session_token: str
    ) -> str:
        """Method to get auth code.

        Args:
            config_file (VcliConfigFile): config file content.
            credential_file (VcliCredentialFile): credential file content.
            code_challenge (str): [description]
            session_token (str): [description]

        Raises:
            AccessTokenFailedError: raises when failed to retrieve access token

        Returns:
            str: Authorization Code
        """
        state = uuid.uuid4()
        nonce = secrets.token_urlsafe(32)
        scope = "openid profile email"
        redirect_url = f"{config_file.service_endpoint}/{REDIRECT_URL_CONSTANT}"
        client_id = credential_file.client_id
        okta_url = credential_file.auth_endpont
        url = f"{okta_url}/oauth2/default/v1/authorize?client_id={client_id}&response_type=code&response_mode=form_post&scope={scope}&redirect_uri={redirect_url}&state={state}&nonce={nonce}&code_challenge_method=S256&code_challenge={code_challenge}&sessionToken={session_token}"

        response = requests.get(url)

        state_resp = re.findall(r'<input\s+type="hidden"\s+name="state"\s+value="([A-Za-z0-9_\-]*)"\s*/>', response.text)
        code_resp = re.findall(r'<input\s+type="hidden"\s+name="code"\s+value="([A-Za-z0-9_\-]*)"\s*/>', response.text)

        if len(state_resp) == 0 or len(code_resp) == 0:
            logger.info("State parameter or code value is not valid!")
            logger.debug(f"state_resp: {state_resp}")
            logger.debug(f"code_resp: {code_resp}")
            raise AccessTokenFailedError(ErrorMessage.ERROR_STATE_PARAM_VERIFY_FAILED)

        state_value = state_resp[0]
        # Authorization Code
        auth_code = code_resp[0]

        # Verify the state parameter
        if state_value == str(state):
            logger.info("State parameter verified successfully.")
        else:
            logger.info("State parameter is not verified!")
            raise AccessTokenFailedError(ErrorMessage.ERROR_STATE_PARAM_VERIFY_FAILED)

        return auth_code

    def _get_access_token(
        self,
        config_file: VcliConfigFile,
        credential_file: VcliCredentialFile,
        auth_code: str,
        code_verifier: str
    ) -> str:
        """Method to get access token

        Args:
            config_file (VcliConfigFile): config file content.
            credential_file (VcliCredentialFile): credential file content.
            auth_code (str): [description]
            code_verifier (str): [description]

        Returns:
            str: Access token
        """
        redirect_url = f"{config_file.service_endpoint}/{REDIRECT_URL_CONSTANT}"
        client_id = credential_file.client_id
        okta_url = credential_file.auth_endpont
        response = requests.post(
            url=f"{okta_url}/oauth2/default/v1/token",
            data={
                "grant_type": "authorization_code",
                "client_id": client_id,
                "redirect_uri": redirect_url,
                "code": auth_code,
                "code_verifier": code_verifier,
            },
        )
        result = response.json()
        access_token = result["access_token"]
        result.pop('access_token', None)
        result.pop('id_token', None)
        logger.debug(f"Access Token step: {result}")
        return access_token
