import os
import os.path
from datetime import datetime
from uuid import uuid1

from django.conf import settings
from django.forms import model_to_dict

from uboxadmin.authentication import JwtAuthentication
from uboxadmin.exceptions import BadRequest
from uboxadmin.generic import Router, validate_serializer_data_safely
from uboxadmin.models.jwt import BlackListedToken
from uboxadmin.models.system import User
from uboxadmin.serializers import MenuSerializer, PersonUpdateRequest

router = Router()


@router.get("^person$")
def get_person(request):
    data = model_to_dict(request.user)
    del data["password"]
    return data


@router.post("personUpdate")
def update(request):
    serializer = PersonUpdateRequest(data=request.data)
    validate_serializer_data_safely(serializer)
    data = serializer.data
    user = request.user  # type: User

    if "password" in data:
        user.set_password(data.pop("password"))
        user.password_v += 1

    user.__dict__.update(data)
    user.save()
    return {}


@router.get("permmenu")
def get_permenu(request):
    serializer = MenuSerializer(request.user.menus, many=True)
    return {"perms": request.user.permissions, "menus": serializer.data}


@router.post("upload$", "uboxadmin.base.comm.upload")
def upload(request):
    if not request.FILES:
        raise BadRequest(message="上传文件不能为空")

    file = request.FILES["file"]
    extension = os.path.splitext(file.name)[1]
    today = datetime.today()
    name = today.strftime("%Y%m%d") + '/' + str(uuid1()) + extension

    target = os.path.join(settings.MEDIA_ROOT, f"uploads/{name}")
    dir_path = os.path.join(settings.MEDIA_ROOT, f"uploads/{today.strftime('%Y%m%d')}")

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    with open(target, "wb") as fp:
        fp.write(file.read())

    return os.path.join(settings.MEDIA_URL, f"uploads/{name}")


@router.get("uploadMode")
def get_upload_mode(request):
    return {"mode": "local", "type": "local"}


jwt_authentication = JwtAuthentication()


@router.post("logout")
def logout(request):
    header = jwt_authentication.get_header(request)
    token = jwt_authentication.get_raw_token(header)
    BlackListedToken.add(request.user, token.decode())
    return {}
