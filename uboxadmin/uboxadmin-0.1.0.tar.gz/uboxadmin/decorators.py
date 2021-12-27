import json
from functools import update_wrapper
from types import FunctionType

from django.http.response import HttpResponseBase
from rest_framework.views import APIView

from uboxadmin.models.system import Log
from uboxadmin.utils import get_client_ip, make_response
from uboxadmin.view_conf import APIViewConf


def log(func):
    def wrapper(request, *args, **kwargs):
        if request.method.lower() == "get":
            params = json.dumps(request.GET.dict())
        else:
            params = getattr(request, "data", None)
            if not params:
                params = ""

        Log.record(get_client_ip(request), request.get_full_path(), params, request.user.id)
        return func(request, *args, **kwargs)

    update_wrapper(wrapper, func)
    return wrapper


def api_view(http_method_names=None):
    """
    Decorate a function as a view handler which are wrapped into APIView subclass.
    basic configuration classes are installed by APIViewConf class.
    """
    http_method_names = ["GET"] if (http_method_names is None) else http_method_names

    def decorator(func):
        WrappedAPIView = type(
            "WrappedAPIView",
            (
                APIViewConf,
                APIView,
            ),
            {"__doc__": func.__doc__},
        )

        # api_view applied without (method_names)
        assert not (isinstance(http_method_names, FunctionType)), "@api_view missing list of allowed HTTP methods"

        # api_view applied with eg. string instead of list of strings
        assert isinstance(http_method_names, (list, tuple)), (
            "@api_view expected a list of strings, received %s" % type(http_method_names).__name__
        )

        allowed_methods = set(http_method_names) | {"options"}
        WrappedAPIView.http_method_names = [method.lower() for method in allowed_methods]

        def handler(self, *args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, HttpResponseBase):
                return result
            if isinstance(result, tuple):
                data, code = result
                return make_response(data, code)
            else:
                return make_response(result)

        for method in http_method_names:
            setattr(WrappedAPIView, method.lower(), handler)

        WrappedAPIView.__name__ = func.__name__
        WrappedAPIView.__module__ = func.__module__

        WrappedAPIView.renderer_classes = getattr(func, "renderer_classes", WrappedAPIView.renderer_classes)

        WrappedAPIView.parser_classes = getattr(func, "parser_classes", WrappedAPIView.parser_classes)

        WrappedAPIView.authentication_classes = getattr(
            func, "authentication_classes", WrappedAPIView.authentication_classes
        )

        WrappedAPIView.throttle_classes = getattr(func, "throttle_classes", WrappedAPIView.throttle_classes)

        WrappedAPIView.permission_classes = getattr(func, "permission_classes", WrappedAPIView.permission_classes)

        WrappedAPIView.schema = getattr(func, "schema", WrappedAPIView.schema)

        return log(WrappedAPIView.as_view())

    return decorator
