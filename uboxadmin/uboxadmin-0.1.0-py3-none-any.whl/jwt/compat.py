import jwt
from rest_framework_simplejwt.backends import TokenBackend as _TokenBackend
from rest_framework_simplejwt.settings import api_settings


class TokenBackend(_TokenBackend):
    def encode(self, payload):
        """
        Returns an encoded token for the given payload dictionary.
        """
        jwt_payload = payload.copy()
        token = jwt.encode(jwt_payload, self.signing_key, algorithm=self.algorithm)  # type: ignore
        if isinstance(token, bytes):
            # For PyJWT <= 1.7.1
            return token.decode("utf-8")
        # For PyJWT >= 2.0.0a1
        return token


token_backend = TokenBackend(
    api_settings.ALGORITHM, api_settings.SIGNING_KEY, api_settings.VERIFYING_KEY
)
