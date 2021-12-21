#
#  (c) Copyright 2021 Micro Focus or one of its affiliates.
#

import os
from dataclasses import dataclass
from configparser import ConfigParser
from vcli.util.vcli_logger import logger
from vcli.constant import VCLI_CONFIG_PATH, VCLI_CREDENTIAL_FILE, VCLI_USER, VCLI_PASSWORD
from vcli.exceptions.vcli_custom_exception import ValidationFailedError, ProfileNotExistError, ProfilePermissionError, AccessTokenFailedError
from vcli.util.error_message import ErrorMessage


@dataclass
class VcliCredentialFile:
    username: str
    password: str
    client_id: str
    auth_endpont: str
    access_token_file: str = ""

    def __post_init__(self):
        """Validation method

        Raises:
            ValidationFailedError: raise when required param is not provided
        """
        if not self.username:
            err_msg = ErrorMessage.USERNAME_CAN_NOT_BE_NONE
            logger.error(err_msg)
            raise ValidationFailedError(err_msg)
        if not self.password:
            err_msg = ErrorMessage.PASSWORD_CAN_NOT_BE_NONE
            logger.error(err_msg)
            raise ValidationFailedError(err_msg)
        if not self.client_id:
            err_msg = ErrorMessage.OKTA_CLIENT_CAN_NOT_BE_NONE
            logger.error(err_msg)
            raise ValidationFailedError(err_msg)
        if not self.auth_endpont:
            err_msg = ErrorMessage.OKTA_AUTH_ENDPOINT_CAN_NOT_BE_NONE
            logger.error(err_msg)
            raise ValidationFailedError(err_msg)

    def write_config(self, profile: str):
        """method to write data class data to config file

        Args:
            profile (str): section defined in the config file
        """
        credential_writer = ConfigParser()
        credential_writer.read(f"{VCLI_CONFIG_PATH}/{VCLI_CREDENTIAL_FILE}")
        is_profile_exist = credential_writer.has_section(profile)
        if not is_profile_exist:
            credential_writer.add_section(profile)
        credential_writer.set(profile, 'username', self.username)
        credential_writer.set(profile, 'password', self.password)
        credential_writer.set(profile, 'client_id', self.client_id)
        credential_writer.set(profile, 'auth_endpont', self.auth_endpont)

        with open(f"{VCLI_CONFIG_PATH}/{VCLI_CREDENTIAL_FILE}", 'w') as credential_file:
            credential_writer.write(credential_file)

    def get_access_token(self, profile: str) -> str:
        """Get access_token value from certain profile section

        Args:
            profile (str): section defined in the config file

        Raises:
            ProfileNotExistError: Raises when profile is not found
            AccessTokenFailedError: Raises when access token file is not found

        Returns:
            [str]: access_token value
        """
        credential_writer = ConfigParser()
        credential_writer.read(f"{VCLI_CONFIG_PATH}/{VCLI_CREDENTIAL_FILE}")
        is_profile_exist = credential_writer.has_section(profile)
        if not is_profile_exist:
            raise ProfileNotExistError(f"credential file section profile: {profile} does not exist")
        access_token_file = credential_writer.get(profile, 'access_token_file', fallback=None)
        access_token = ""
        if access_token_file is None:
            raise AccessTokenFailedError(ErrorMessage.ERROR_ACCESS_TOKEN_FILE_NOT_FOUND)

        if not os.path.exists(f"{VCLI_CONFIG_PATH}/{access_token_file}"):
            with open(f"{VCLI_CONFIG_PATH}/{VCLI_CREDENTIAL_FILE}", 'w') as credential_file:
                credential_writer.remove_option(profile, 'access_token_file')
                credential_writer.write(credential_file)
            raise ProfileNotExistError(ErrorMessage.ERROR_ACCESS_TOKEN_FILE_NOT_FOUND)

        with open(f"{VCLI_CONFIG_PATH}/{access_token_file}", 'r') as access_token_file_content:
            access_token = access_token_file_content.read()

        return access_token

    def update_access_token(self, access_token: str, profile: str):
        """Update the value for access_token file for certain profile section

        Args:
            access_token (str): okta access token
            profile (str): section defined in the config file
        """
        credential_writer = ConfigParser()
        credential_writer.read(f"{VCLI_CONFIG_PATH}/{VCLI_CREDENTIAL_FILE}")
        is_profile_exist = credential_writer.has_section(profile)
        if not is_profile_exist:
            credential_writer.add_section(profile)
        credential_writer.set(profile, 'access_token_file', f"access_token_file_{profile}")

        with open(f"{VCLI_CONFIG_PATH}/access_token_file_{profile}", 'w') as access_token_file:
            access_token_file.write(access_token)

        with open(f"{VCLI_CONFIG_PATH}/{VCLI_CREDENTIAL_FILE}", 'w') as credential_file:
            credential_writer.write(credential_file)

    def delete_access_token(self, profile: str):
        """Delete access token file attribute under config file

        Args:
            profile (str): section defined in the config file
        """
        credential_writer = ConfigParser()
        credential_writer.read(f"{VCLI_CONFIG_PATH}/{VCLI_CREDENTIAL_FILE}")
        is_profile_exist = credential_writer.has_section(profile)
        if not is_profile_exist:
            credential_writer.add_section(profile)
        credential_writer.remove_option(profile, 'access_token_file')

        with open(f"{VCLI_CONFIG_PATH}/{VCLI_CREDENTIAL_FILE}", 'w') as credential_file:
            credential_writer.write(credential_file)

        if os.path.exists(f"{VCLI_CONFIG_PATH}/access_token_file_{profile}"):
            os.remove(f"{VCLI_CONFIG_PATH}/access_token_file_{profile}")

    @staticmethod
    def read_profile_config(profile: str):
        """read config file and return it as a data class model

        Args:
            profile (str): section defined in the config file

        Raises:
            ProfileNotExistError: raise when section not exists in config file

        Returns:
            VcliCredentialFile: this class
        """
        config_reader = ConfigParser()
        config_reader.read(f"{VCLI_CONFIG_PATH}/{VCLI_CREDENTIAL_FILE}")
        is_profile_exist = config_reader.has_section(profile)
        if not is_profile_exist:
            raise ProfileNotExistError(f"credential file section profile: {profile} does not exist")
        conf_dict = {section: dict(config_reader.items(section)) for section in config_reader.sections()}
        if VCLI_USER:
            logger.info(f"Env param VCLI_USER detected, using {VCLI_USER} as username")
            username = VCLI_USER
        else:
            username = conf_dict.get(profile, {}).get('username')
        if VCLI_PASSWORD:
            logger.info("Env param VCLI_PASSWORD detected, using that as password")
            password = VCLI_PASSWORD
        else:
            password = conf_dict.get(profile, {}).get('password')
        return VcliCredentialFile(
            username=username,
            password=password,
            client_id=conf_dict.get(profile).get('client_id'),
            auth_endpont=conf_dict.get(profile).get('auth_endpont'),
            access_token_file=conf_dict.get(profile).get('access_token_file')
        )

    @staticmethod
    def check_profile_file(profile: str):
        """check if config file is valid.

        Args:
            profile (str): section defined in the config file

        Raises:
            ProfilePermissionError: raise when profile is not readable or writeable
            ProfileNotExistError: raise when section not exists in config file
        """
        if not os.path.exists(f"{VCLI_CONFIG_PATH}/{VCLI_CREDENTIAL_FILE}"):
            raise ProfileNotExistError(ErrorMessage.ERROR_CREDENTIAL_CONFIG_NOT_EXIST)
        if not os.access(f"{VCLI_CONFIG_PATH}/{VCLI_CREDENTIAL_FILE}", os.R_OK):
            raise ProfilePermissionError(ErrorMessage.ERROR_CREDENTIAL_CONFIG_NOT_READABLE)
        if not os.access(f"{VCLI_CONFIG_PATH}/{VCLI_CREDENTIAL_FILE}", os.W_OK):
            raise ProfilePermissionError(ErrorMessage.ERROR_CREDENTIAL_CONFIG_NOT_WRITEABLE)
