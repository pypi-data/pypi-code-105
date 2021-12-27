from typing import Dict, Optional

from django.contrib.auth.base_user import AbstractBaseUser
from rest_framework import serializers
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from typing_extensions import TypedDict

from uboxadmin.exceptions import AuthenticationFailed
from uboxadmin.models.system import User
from uboxadmin.utils import make_response_content


class TokenObtainRequest(TypedDict):
    username: str
    password: str


class TokenRefreshRequest(TypedDict):
    refresh: str


class TokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = PasswordField()

    @classmethod
    def get_token(cls, user):
        # type: (AbstractBaseUser) -> RefreshToken
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        # type: (TokenObtainRequest) -> Dict
        try:
            user = User.objects.get(**{User.USERNAME_FIELD: attrs["username"]})  # type: Optional[User]
        except User.DoesNotExist:
            user = None

        if user is None or not user.is_active:
            raise AuthenticationFailed(message="账户未激活")

        if not user.check_password(attrs["password"]):
            raise AuthenticationFailed(message="密码错误")

        self.user = user

        refresh = self.get_token(self.user)

        data = {}
        data["refresh_token"] = str(refresh)
        access_token = refresh.access_token
        data["token"] = str(access_token)
        data["expire"] = access_token.lifetime.total_seconds()  # type: ignore
        data["refresh_expire"] = refresh.lifetime.total_seconds()  # type: ignore

        return make_response_content(data)


class TokenRefreshSerializer(serializers.Serializer):
    refreshToken = serializers.CharField()

    def validate(self, attrs):
        refresh = RefreshToken(attrs["refreshToken"])

        access_token = refresh.access_token
        data = {"token": str(access_token), "expire": access_token.lifetime.total_seconds()}  # type: ignore

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data["refreshToken"] = str(refresh)
            data["refreshExpire"] = refresh.lifetime.total_seconds()  # type: ignore

        return make_response_content(data)
