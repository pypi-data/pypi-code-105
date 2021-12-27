from typing import Optional

from django.utils.translation import gettext_lazy as _
from rest_framework import status

from uboxadmin.defines import ResponseCode


class AdminException(Exception):
    http_status_code = status.HTTP_200_OK
    admin_status_code = ResponseCode.OK
    message: str

    def __init__(self, admin_status_code=None, message=None, http_status_code=None) -> None:
        # type: (Optional[ResponseCode], Optional[str], Optional[int]) -> None
        self.http_status_code = http_status_code if http_status_code is not None else self.http_status_code
        self.admin_status_code = admin_status_code if admin_status_code is not None else self.admin_status_code
        self.message = message if message is not None else self.admin_status_code.description


class NotFound(AdminException):
    admin_status_code = ResponseCode.NOT_FOUND


class BadRequest(AdminException):
    admin_status_code = ResponseCode.BAD_REQUEST


class AuthenticationFailed(AdminException):
    admin_status_code = ResponseCode.AUTHENTICATION_FAILED


class ArgsRequiredError(AdminException):
    admin_status_code = ResponseCode.ARGS_REQUIRED
    default_message = _("fields {fields} required")

    def __init__(self, *fields, http_status_code=None) -> None:
        # type: (str, Optional[int]) -> None
        message = self.default_message.format(fields=", ".join(fields))
        super().__init__(message=message, http_status_code=http_status_code)
