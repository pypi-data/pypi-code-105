#
#  (c) Copyright 2021 Micro Focus or one of its affiliates.
#

from typing import Optional
from vcli.util.error_message import ErrorMessage


class BaseCustomException(Exception):
    """Custom exception defined for VA"""
    msg: str = ErrorMessage.GENERAL_ERROR
    error_code: int = 1

    def __init__(self, msg: str, error_code: Optional[int] = None):           
        super().__init__(msg)
        self.msg = msg
        if error_code is not None:
            self.error_code = error_code

    def __str__(self):
        return f"{self.msg}, with error_code: {self.error_code}"


class ValidationFailedError(BaseCustomException):
    """Raised when the input value is not valid"""
    msg: str = "Validation error"
    error_code: int = 1


class ProfileNotExistError(BaseCustomException):
    """Raised when section does not exists in config file"""
    msg: str = "Profile does not exist"
    error_code: int = 1


class ProfilePermissionError(BaseCustomException):
    """Raised when config permission is not valid"""
    msg: str = "Config can not be read or write"
    error_code: int = 1


class AccessTokenFailedError(BaseCustomException):
    """Raised when access token is not valid"""
    msg: str = "Failed to verify access token, please login again"
    error_code: int = 1
