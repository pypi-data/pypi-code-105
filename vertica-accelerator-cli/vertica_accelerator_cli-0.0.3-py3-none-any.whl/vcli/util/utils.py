#
#  (c) Copyright 2021 Micro Focus or one of its affiliates.
#

import ssl
import argparse
import requests
import urllib3
from copy import deepcopy
from urllib.parse import urlparse
from datetime import datetime as dt, timedelta as td
from openapi_client.configuration import Configuration
from openapi_client.api_client import ApiClient
from vcli.models.vcli_config_file import VcliConfigFile
from vcli.models.vcli_credential_file import VcliCredentialFile
from vcli.constant import (
    MIN_DB_NAME_LENGTH,
    MAX_DB_NAME_LENGTH,
    MIN_DNS_NAME_LENGTH,
    MAX_DNS_NAME_LENGTH,
    MAX_CRON_NAME_LENGTH,
    OA_SERVICE_PROXY_SURFFIX
)
from vcli.util.static_params import (
    VALID_REPORT_RANGE
)
from vcli.util.vcli_logger import logger
from vcli.exceptions.vcli_custom_exception import AccessTokenFailedError
from vcli.util.error_message import ErrorMessage


def build_api_client(profile: str) -> ApiClient:
    """Method to build an openapi client

    Args:
        profile (str): vaas user profile from commndline.

    Returns:
        ApiClient: openapi client
    """
    urllib3.disable_warnings()
    config_file = VcliConfigFile.read_profile_config(profile=profile)
    credential_file = VcliCredentialFile.read_profile_config(profile=profile)

    api_config = Configuration(host=f"{config_file.service_endpoint}/{OA_SERVICE_PROXY_SURFFIX}", ssl_ca_cert=ssl.CERT_NONE)
    api_config.verify_ssl = str_to_bool(config_file.verify_ssl)
    api_client = ApiClient(configuration=api_config)
    api_client.default_headers['Authorization'] = credential_file.get_access_token(profile=profile)
    return api_client


def verify_access_token(credential_file: VcliCredentialFile, profile: str, access_token: str = ""):
    """Method to verify access token

    Args:
        credential_file (VcliCredentialFile): credential file content.
        profile (str): vaas user profile from commndline.
        access_token (str, optional): access toekn to be verified, if not provided, will be read from credential_file. Defaults to "".

    Raises:
        AccessTokenFailedError: Rasies access token failed to verified(expired or file not found). 
    """
    if not access_token:
        access_token = credential_file.get_access_token(profile=profile)
    okta_url = credential_file.auth_endpont
    client_id = credential_file.client_id
    url = f"{okta_url}/oauth2/default/v1/introspect"
    payload = f"client_id={client_id}&token={access_token}&token_type_hint=access_token"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post(url, headers=headers, data=payload)
    result = response.json()
    # Verify access_token
    if response.status_code == 200 and result["active"] is True:
        logger.info("Token verified successfully.")
        credential_file.update_access_token(access_token=access_token, profile=profile)
    else:
        logger.info("Error in verifying the access_token!")
        credential_file.delete_access_token(profile=profile)
        raise AccessTokenFailedError(ErrorMessage.ERROR_VERIFY_ACCESS_TOKEN_FAIL)


def log_arg_func(func):
    """Make a deep copy and log the cmd info, so pop won't affect the following run.

    Args:
        func ([type]): [description]
    """
    func_info = deepcopy(vars(func))
    sensitive_info = ['password']
    for arg in sensitive_info:
        func_info.pop(arg, None)
    logger.info(f"Running cmd: {func_info.pop('func', None)} with args: {func_info}")


def str_to_bool(input: str) -> bool:
    """
    Convert string to bool

    Args:
        input (str): Input from the user

    Raises:
        ArgumentTypeError: Raise when the input is not in boolean form

    Returns:
        bool: Returns boolean flag according to given input
    """
    if isinstance(input, bool):
        return input
    if input.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif input.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def cron_name_validate(input: str) -> str:
    """
    Validate cron job name

    Args:
        input (str): Input from the user

    Raises:
        ArgumentTypeError: Raise when the input is not in boolean form

    Returns:
        input (str): Input from the user
    """
    if len(input) <= MAX_CRON_NAME_LENGTH:
        return input
    else:
        raise argparse.ArgumentTypeError(f'The maximum cron job name length is {MAX_CRON_NAME_LENGTH} characters.')


def get_date_time(range: str) -> tuple:
    """
    Convert given time range into date time format

    Args:
        range (str): Time range of the report (e.g. '1 hour')

    Returns:
        tuple(start_date_time, end_date_time): start and end date corresponding to time range
                                            (e.g. 2021-12-01 06:24:08.785623, 2021-12-01 07:24:08.785623)
    """
    if range == VALID_REPORT_RANGE.THREE_MONTH.value:
        end_date_time = dt.utcnow()
        start_date_time = end_date_time - td(days=90)
    elif range == VALID_REPORT_RANGE.ONE_MONTH.value:
        end_date_time = dt.utcnow()
        start_date_time = end_date_time - td(days=30)
    elif range == VALID_REPORT_RANGE.ONE_WEEK.value:
        end_date_time = dt.utcnow()
        start_date_time = end_date_time - td(weeks=1)
    elif range == VALID_REPORT_RANGE.ONE_DAY.value:
        end_date_time = dt.utcnow()
        start_date_time = end_date_time - td(days=1)
    elif range == VALID_REPORT_RANGE.EIGHT_HOURS.value:
        end_date_time = dt.utcnow()
        start_date_time = end_date_time - td(hours=8)
    elif range == VALID_REPORT_RANGE.ONE_HOUR.value:
        end_date_time = dt.utcnow()
        start_date_time = end_date_time - td(hours=1)
    return start_date_time, end_date_time


def db_name_validate(input: str) -> str:
    """
    Validate database name

    Args:
        input (str): Input from the user

    Raises:
        ArgumentTypeError: Raise when the database name length is not range

    Returns:
        input (str): Input from the user
    """
    if len(input) in range(MIN_DB_NAME_LENGTH, MAX_DB_NAME_LENGTH + 1):
        return input
    else:
        raise argparse.ArgumentTypeError(f'Database name must be {MIN_DB_NAME_LENGTH} to {MAX_DB_NAME_LENGTH} lower alpha-numeric characters, starting with a letter.')


def dns_name_validate(input: str) -> str:
    """
    Validate DNS name

    Args:
        input (str): Input from the user

    Raises:
        ArgumentTypeError: Raise when the DNS name length is not range

    Returns:
        input (str): Input from the user
    """
    if len(input) in range(MIN_DNS_NAME_LENGTH, MAX_DNS_NAME_LENGTH + 1):
        return input
    else:
        raise argparse.ArgumentTypeError(f'DNS name must be {MIN_DNS_NAME_LENGTH} to {MAX_DNS_NAME_LENGTH} lower alpha-numeric characters, starting with a letter.')


def http_name_validate(url: str) -> str:
    """
    Validate http url

    Args:
        url (str): Input from the user

    Raises:
        ArgumentTypeError: Raise when url doesn't contains http

    Returns:
        url (str): Input from the user
    """
    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            return url
    except ValueError:
        pass
    raise argparse.ArgumentTypeError('Please provide an valid url form. For example: https://vertica.okta.com')
