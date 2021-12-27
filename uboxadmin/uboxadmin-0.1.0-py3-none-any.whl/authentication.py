from io import BytesIO
from random import choice
from typing import Optional

from django.utils.translation import ugettext_lazy as _
from rest_framework_simplejwt.authentication import AUTH_HEADER_TYPE_BYTES, JWTAuthentication as _JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken

from uboxadmin.defines import UserStatus
from uboxadmin.models.jwt import BlackListedToken
from uboxadmin.models.system import User


class JwtAuthentication(_JWTAuthentication):
    def get_user(self, validated_token):
        # type: (AccessToken) -> Optional[User]
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken(_("Token contained no recognizable user identification"))

        try:
            user: User = User.objects.get(**{api_settings.USER_ID_FIELD: user_id})  # type: ignore
        except User.DoesNotExist:
            raise AuthenticationFailed(_("User not found"), code="user_not_found")

        if user.STATUS == UserStatus.DISABLED:
            raise AuthenticationFailed(_("User is inactive"), code="user_inactive")

        if BlackListedToken.is_blacklisted(user, validated_token):
            raise AuthenticationFailed(_("Token is blacklisted"), code="blacklist_token")

        return user

    def get_raw_token(self, header):
        for bs in AUTH_HEADER_TYPE_BYTES:
            if bs in header:
                break
        else:
            buf = BytesIO()
            buf.write(choice(tuple(AUTH_HEADER_TYPE_BYTES)))
            buf.write(b" ")
            buf.write(header)
            header = buf.getvalue()

        return super().get_raw_token(header)
