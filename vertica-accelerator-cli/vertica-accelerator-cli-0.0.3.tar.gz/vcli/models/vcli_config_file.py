#
#  (c) Copyright 2021 Micro Focus or one of its affiliates.
#

import os
from dataclasses import dataclass
from configparser import ConfigParser
from vcli.util.vcli_logger import logger
from vcli.constant import VCLI_CONFIG_PATH, VCLI_CONFIG_FILE, MAX_ATTEMPTS_DEFAULT
from vcli.exceptions.vcli_custom_exception import ValidationFailedError, ProfileNotExistError, ProfilePermissionError
from vcli.util.error_message import ErrorMessage


@dataclass
class VcliConfigFile:
    service_endpoint: str
    max_attempts: int = MAX_ATTEMPTS_DEFAULT
    verify_ssl: bool = True
    vertica_version: str = ""
    region: str = ""

    def __post_init__(self):
        """Validation method

        Raises:
            ValidationFailedError: raise when required param is not provided
        """
        if not self.service_endpoint:
            err_msg = ErrorMessage.OA_SERVICE_CAN_NOT_BE_NONE
            logger.error(err_msg)
            raise ValidationFailedError(err_msg)
        if not self.max_attempts:
            self.max_attempts = str(MAX_ATTEMPTS_DEFAULT)

    def write_config(self, profile: str):
        """method to write data class data to config file

        Args:
            profile (str): section defined in the config file
        """
        config_writer = ConfigParser()
        config_writer.read(f"{VCLI_CONFIG_PATH}/{VCLI_CONFIG_FILE}")
        is_profile_exist = config_writer.has_section(profile)
        if not is_profile_exist:
            config_writer.add_section(profile)
        config_writer.set(profile, 'service_endpoint', self.service_endpoint)
        config_writer.set(profile, 'max_attempts', str(self.max_attempts))
        config_writer.set(profile, 'verify_ssl', str(self.verify_ssl).lower())

        with open(f"{VCLI_CONFIG_PATH}/{VCLI_CONFIG_FILE}", 'w') as configfile:
            config_writer.write(configfile)

    @staticmethod
    def read_profile_config(profile: str):
        """read config file and return it as a data class model

        Args:
            profile (str): section defined in the config file

        Raises:
            ProfilePermissionError: raise when profile is not readable or writeable

        Returns:
            VcliConfigFile: this class
        """
        config_reader = ConfigParser()
        config_reader.read(f"{VCLI_CONFIG_PATH}/{VCLI_CONFIG_FILE}")
        is_profile_exist = config_reader.has_section(profile)
        if not is_profile_exist:
            raise ProfileNotExistError(f"config file section profile: {profile} does not exist")
        conf_dict = {section: dict(config_reader.items(section)) for section in config_reader.sections()}
        return VcliConfigFile(
            service_endpoint=conf_dict.get(profile, {}).get('service_endpoint'),
            max_attempts=conf_dict.get(profile).get('max_attempts'),
            vertica_version=conf_dict.get(profile).get('vertica_version'),
            region=conf_dict.get(profile).get('region'),
            verify_ssl=conf_dict.get(profile).get('verify_ssl', True)
        )

    @staticmethod
    def check_profile_file(profile: str):
        """check if config file is valid.

        Args:
            profile (str): section defined in the config file

        Raises:
            ProfilePermissionError: raise when profile is not readable or writeable
            ProfileNotExistError: raise when section not exists in config file

        Returns:
            VcliConfigFile: this class
        """
        if not os.path.exists(f"{VCLI_CONFIG_PATH}/{VCLI_CONFIG_FILE}"):
            raise ProfileNotExistError(ErrorMessage.ERROR_CONFIG_CONFIG_NOT_EXIST)
        if not os.access(f"{VCLI_CONFIG_PATH}/{VCLI_CONFIG_FILE}", os.R_OK):
            raise ProfilePermissionError(ErrorMessage.ERROR_CONFIG_CONFIG_NOT_READABLE)
        if not os.access(f"{VCLI_CONFIG_PATH}/{VCLI_CONFIG_FILE}", os.W_OK):
            raise ProfilePermissionError(ErrorMessage.ERROR_CONFIG_CONFIG_NOT_WRITEABLE)
