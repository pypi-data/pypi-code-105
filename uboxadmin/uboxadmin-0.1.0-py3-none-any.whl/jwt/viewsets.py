from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView as _TokenObtainPairView

from uboxadmin.generic import APIViewConf

from .serializers import TokenObtainSerializer, TokenRefreshSerializer


class TokenObtainPairView(APIViewConf, _TokenObtainPairView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = TokenObtainSerializer


class TokenRefreshView(APIViewConf, _TokenObtainPairView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = TokenRefreshSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.query_params.dict()
        )  # type: Serializer

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
