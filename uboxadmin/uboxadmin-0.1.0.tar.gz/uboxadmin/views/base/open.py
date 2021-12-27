from base64 import b64encode
from random import choice
from uuid import uuid4

from captcha.image import ImageCaptcha
from rest_framework.decorators import authentication_classes, permission_classes

from uboxadmin.generic import Router
from uboxadmin.jwt.viewsets import TokenObtainPairView, TokenRefreshView
from uboxadmin.serializers import CaptchaRequest
from uboxadmin.settings import admin_settings

router = Router()
router.register("login", TokenObtainPairView.as_view())
router.register("refreshToken", TokenRefreshView.as_view())


@router.get("captcha")
@authentication_classes(())
@permission_classes(())
def get_captcha(request):
    serializer = CaptchaRequest(data=request.query_params.dict())
    serializer.is_valid(True)
    data = serializer.data

    uuid = uuid4()
    capcha = ImageCaptcha(width=data["width"], height=data["height"])
    data = capcha.generate("".join([choice(admin_settings.CAPTCHA_CHARS) for _ in range(4)]))  # type: ignore
    return {
        "captchaId": str(uuid),
        "data": 'data: image/png;base64,%s'
        % b64encode(data.getvalue()).decode(),
    }
