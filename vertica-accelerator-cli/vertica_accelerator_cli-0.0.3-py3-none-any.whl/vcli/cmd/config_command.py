#!/bin/python3
# coding=utf-8
# ------------------------------------------------------------------------------
# Created on October 05 12:58 2021
#
# Vertica Vaas Okta config command
#
# Usage:
#   va config
#   va config set --username abcd --profile profile1
#
# (c) Copyright 2021 Micro Focus or one of its affiliates.
# ------------------------------------------------------------------------------
from argparse import Namespace
from getpass import getpass
from vcli.cmd.sub_command import SubCommandImplementation
from vcli.constant import VCLI_CONFIG_DEFAULT
from vcli.models.vcli_config_file import VcliConfigFile
from vcli.models.vcli_credential_file import VcliCredentialFile
from vcli.exceptions.vcli_custom_exception import ValidationFailedError
from vcli.util.error_message import ErrorMessage
from vcli.util.help_message import HelpMessage
from vcli.util.utils import http_name_validate, str_to_bool


class ConfigCommand(SubCommandImplementation):
    def operation_define(self, subparsers) -> None:
        # Supported command line options:
        #   va config
        #   va config set --username abcd --profile profile1
        config_parser = subparsers.add_parser('config', help=HelpMessage.config_header)
        config_set = config_parser.add_subparsers()

        # set command
        config_set_parser = config_set.add_parser('set', help=HelpMessage.config_set)
        config_set_parser.add_argument('--username', metavar='<value>', type=str, help=HelpMessage.set_username)
        config_set_parser.add_argument('--password', metavar='<value>', type=str, help=HelpMessage.set_password)
        config_set_parser.add_argument('--client_id', metavar='<value>', type=str, help=HelpMessage.set_client_id)
        config_set_parser.add_argument('--auth_endpont', metavar='<value>', type=http_name_validate, help=HelpMessage.set_auth_endpont)
        config_set_parser.add_argument('--service_endpoint', metavar='<value>', type=http_name_validate, help=HelpMessage.set_service_endpoint)
        config_set_parser.add_argument('--max_attempts', metavar='<value>', type=int, help=HelpMessage.set_max_attempts)
        config_set_parser.add_argument('--verify_ssl', metavar='<value>', default=True, required=False, type=str_to_bool, help=HelpMessage.set_verify_ssl)
        config_set_parser.add_argument('--profile', default=VCLI_CONFIG_DEFAULT, metavar='<value>', type=str, help=HelpMessage.profile)
        config_set_parser.set_defaults(func=self.operation_set_detail)

        config_parser.add_argument('--profile', default=VCLI_CONFIG_DEFAULT, metavar='<value>', type=str, help=HelpMessage.profile)
        config_parser.set_defaults(func=self.operation_cmd)

    def operation_cmd(self, args: Namespace) -> None:
        vcli_config_data, vcli_credential_data = ConfigCommand.read_user_input_all(args=args)
        ConfigCommand.set_config_data(
            vcli_config_data=vcli_config_data,
            vcli_credential_data=vcli_credential_data,
            profile=args.profile
        )
        print("Config update success")

    def operation_set_detail(self, args: Namespace) -> None:
        vcli_config_data, vcli_credential_data = ConfigCommand.read_user_input_detail(args=args)
        ConfigCommand.set_config_data(
            vcli_config_data=vcli_config_data,
            vcli_credential_data=vcli_credential_data,
            profile=args.profile
        )
        print("Config update success")

    @staticmethod
    def set_config_data(vcli_config_data: VcliConfigFile, vcli_credential_data: VcliCredentialFile, profile: str):
        """Read config data and write to config file

        Args:
            vcli_config_data (VcliConfigFile): [description]
            vcli_credential_data (VcliCredentialFile): [description]
            profile (str): [description]
        """
        vcli_config_data.write_config(profile=profile)
        vcli_credential_data.write_config(profile=profile)

    @staticmethod
    def read_user_input_all(args: Namespace) -> [VcliConfigFile, VcliCredentialFile]:
        """Help method to read user input and validate the data

        Args:
            args (Namespace): args passed down from cmd

        Returns:
            [VcliConfigFile, VcliCredentialFile]: Validated config data
        """
        username = input("Login username (required. e.g. user@domain.com): ")
        if not username:
            raise ValidationFailedError(msg=ErrorMessage.USERNAME_CAN_NOT_BE_NONE)
        password = getpass("Login password (required): ")
        if not password:
            raise ValidationFailedError(msg=ErrorMessage.PASSWORD_CAN_NOT_BE_NONE)
        client_id = input("Client id (required): ")
        if not client_id:
            raise ValidationFailedError(msg=ErrorMessage.OKTA_CLIENT_CAN_NOT_BE_NONE)
        auth_endpont = input("Authentication endpoint (required. e.g: https://vertica.okta.com): ")
        if not auth_endpont:
            raise ValidationFailedError(msg=ErrorMessage.OKTA_AUTH_ENDPOINT_CAN_NOT_BE_NONE)
        service_endpoint = input("Service endpoint (required, e.g. https://accelerator.vertica.com): ")
        if not service_endpoint:
            raise ValidationFailedError(msg=ErrorMessage.OA_SERVICE_CAN_NOT_BE_NONE)
        max_attempts = input("Max attempts(optional, if empty set to 3): ")

        vcli_config_data = VcliConfigFile(
            service_endpoint=service_endpoint,
            max_attempts=max_attempts
        )
        vcli_credential_data = VcliCredentialFile(
            username=username,
            password=password,
            client_id=client_id,
            auth_endpont=auth_endpont
        )
        return vcli_config_data, vcli_credential_data

    @staticmethod
    def read_user_input_detail(args: Namespace) -> [VcliConfigFile, VcliCredentialFile]:
        """Help method to read user input and validate the data

        Args:
            args (Namespace): args passed down from cmd

        Returns:
            [VcliConfigFile, VcliCredentialFile]: Validated config data
        """
        config_file = VcliConfigFile.read_profile_config(profile=args.profile)
        credential_file = VcliCredentialFile.read_profile_config(profile=args.profile)
        if args.username:
            credential_file.username = args.username
        if args.password:
            credential_file.password = args.password
        if args.auth_endpont:
            credential_file.auth_endpont = args.auth_endpont
        if args.client_id:
            credential_file.client_id = args.client_id
        if args.service_endpoint:
            config_file.service_endpoint = args.service_endpoint
        if args.max_attempts:
            config_file.max_attempts = args.max_attempts
        if args.verify_ssl is not None:
            config_file.verify_ssl = args.verify_ssl
        return config_file, credential_file
