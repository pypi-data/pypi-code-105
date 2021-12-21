#
#  (c) Copyright 2021 Micro Focus or one of its affiliates.
#

class ErrorMessage:
    GENERAL_ERROR = "Something went wrong"
    OA_SERVICE_CAN_NOT_BE_NONE = "service_endpoint can not be empty"
    MAX_ATTEMPTS_CAN_NOT_BE_NONE = "max_attempts can not be empty"
    USERNAME_CAN_NOT_BE_NONE = "username can not be empty"
    PASSWORD_CAN_NOT_BE_NONE = "password can not be empty"
    OKTA_CLIENT_CAN_NOT_BE_NONE = "client_id can not be empty"
    OKTA_AUTH_ENDPOINT_CAN_NOT_BE_NONE = "auth_endpont can not be empty"
    LOGIN_FAILED_BAD_USERNAME_OR_PASSWORD = "Failed to login, please check your okta url, username and password."
    ERROR_CONFIG_CONFIG_NOT_EXIST = "config file does not exists, please run: va config"
    ERROR_CONFIG_CONFIG_NOT_READABLE = "config file can not be read, please check permission"
    ERROR_CONFIG_CONFIG_NOT_WRITEABLE = "config file can not be write, please check permission"
    ERROR_CREDENTIAL_CONFIG_NOT_EXIST = "credential file does not exists, please run: va config"
    ERROR_CREDENTIAL_CONFIG_NOT_READABLE = "credential file can not be read, please check permission"
    ERROR_CREDENTIAL_CONFIG_NOT_WRITEABLE = "credential file can not be write, please check permission"
    ERROR_STATE_PARAM_VERIFY_FAILED = "failed to verify state param"
    ERROR_VERIFY_ACCESS_TOKEN_FAIL = "Error in verifying the access_token, please login and try again."
    ERROR_ACCESS_TOKEN_FILE_NOT_FOUND = "Access token file not found, please login and try again."
