import urllib.parse
from typing import Dict, Optional, Union

from django.http import Http404
from rest_framework import status
from rest_framework.fields import IntegerField
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import exception_handler as _exception_handler, set_rollback

from uboxadmin.defines import ResponseCode
from uboxadmin.exceptions import AdminException, NotFound


def exception_handler(exc, context):
    if isinstance(exc, AdminException):
        set_rollback()
        content = {"code": exc.admin_status_code, "message": exc.message}
        return Response(content, status=exc.http_status_code)
    if isinstance(exc, Http404):
        return exception_handler(NotFound(), context)
    return _exception_handler(exc, context)


def make_response_content(
    data: Optional[Union[dict, list]],
    code: ResponseCode = ResponseCode.OK,
):
    content = {"code": code, "message": code.description}
    if data is not None:
        content["data"] = data
    return content


def make_response(
    data: Optional[Union[dict, list]],
    code: ResponseCode = ResponseCode.OK,
):
    return Response(make_response_content(data, code), status=status.HTTP_200_OK)


def add_url_params(url: str, params: Dict[str, str]) -> str:
    url_parts = list(urllib.parse.urlparse(url))
    query = dict(urllib.parse.parse_qsl(url_parts[4]))
    query.update(params)

    url_parts[4] = urllib.parse.urlencode(query)

    return urllib.parse.urlunparse(url_parts)


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def view_func(method, url_path="", url_name=None):
    def wrapped(func):
        def _wrapped(request, *args, **kwargs):
            return make_response(func(request, *args, **kwargs))

        _wrapped.method = method
        if url_path:
            _wrapped.url_path = url_path
        _wrapped.url_name = url_name
        return _wrapped

    return wrapped


def insert_or_update(model_class, fields, data):
    class Serializer(ModelSerializer):
        id = IntegerField()

        class Meta:
            model = model_class
            fields = "__all__"

    for d in data:
        d = dict(zip(fields, d))

        try:
            inst = model_class.objects.get(id=d["id"])
        except model_class.DoesNotExist:
            inst = None

        serializer = Serializer(inst, data=d)
        serializer.is_valid(True)
        inst = serializer.save()


def merge_dicts(d1, d2):
    # type: (Dict, Dict) -> Dict
    d1 = {k: v for k, v in d1.items()}
    d1.update(d2)
    return d1
