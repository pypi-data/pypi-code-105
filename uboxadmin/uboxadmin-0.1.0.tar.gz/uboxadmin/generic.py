import logging
from functools import update_wrapper
from typing import ClassVar, Generic, List, Optional, Type, TypeVar
from urllib.parse import urljoin

from django.conf.urls import include, url
from django.db.models import Model
from django.db.models.query import QuerySet
from django.db.transaction import atomic
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer, Serializer

from uboxadmin.decorators import api_view, log
from uboxadmin.defines import ParseErrorCode
from uboxadmin.exceptions import ArgsRequiredError, BadRequest
from uboxadmin.settings import admin_settings
from uboxadmin.utils import make_response
from uboxadmin.view_conf import APIViewConf

_T = TypeVar("_T", bound=Model)
logger = logging.getLogger(__file__)


class Router:
    def __init__(self, namespace="") -> None:
        self.namespace = namespace
        self.registry = []

    def register(self, path, func, name=None):
        if name is None:
            self.registry.append((path, func, None))
        else:
            if self.namespace:
                name = f"{self.namespace}.{name}"

            self.registry.append((path, func, name))

        if hasattr(self, "_urls"):
            del self._urls

    def get(self, path, name=None):
        def wrapper(func):
            func = api_view()(func)
            self.register(path, func, name)
            return func

        return wrapper

    def post(self, path, name=None):
        def wrapper(func):
            func = api_view(["POST"])(func)
            self.register(path, func, name)
            return func

        return wrapper

    def get_urls(self):
        return [url(registry[0], registry[1], name=registry[2]) for registry in self.registry]

    @property
    def urls(self):
        if not hasattr(self, "_urls"):
            self._urls = self.get_urls()
        return self._urls


@method_decorator(log, "dispatch")
class ModelViewSet(APIViewConf, GenericAPIView, Generic[_T]):
    queryset: "ClassVar[QuerySet[_T]]"

    ordering_field = admin_settings.DEFAULT_ORDERING_FIELD
    sorting = admin_settings.DEFAULT_SORTING
    pagination_class = admin_settings.DEFAULT_PAGINATION_CLASS
    filter_backends = admin_settings.DEFAULT_FILTER_BACKENDS

    request: Request
    actions = ["add", "delete", "update", "info", "list", "page"]
    lookup_field = "id"

    action_method_map = {
        "add": "post",
        "delete": "post",
        "update": "post",
        "info": "get",
        "list": "post",
        "page": "post",
    }

    _extra_methods = {}

    def add(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        validate_serializer_data_safely(serializer)
        serializer.save()
        return make_response(serializer.data)

    @method_decorator(atomic)
    def delete(self, request, *args, **kwargs):
        try:
            ids = request.data["ids"]
            queryset = self.get_queryset()  # type: QuerySet[_T]
            for entity in queryset.filter(pk__in=ids):
                entity.delete()
            return make_response(None)
        except KeyError:
            raise ArgsRequiredError("ids")

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object_by_lookup_field(request.data[self.lookup_field])
        except KeyError:
            raise ArgsRequiredError(self.lookup_field)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        validate_serializer_data_safely(serializer)
        serializer.save()

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return make_response(serializer.data)

    def info(self, request, *args, **kwargs):
        try:
            instance = self.get_object_by_lookup_field(request.GET[self.lookup_field])
        except KeyError:
            raise ArgsRequiredError(self.lookup_field)
        except Http404:
            return make_response({})

        serializer = self.get_serializer(instance)
        return make_response(serializer.data)

    def _list(self, request, full, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None and not full:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return make_response(serializer.data)

    def list(self, request, *args, **kwargs):
        return self._list(request, True, *args, **kwargs)

    def page(self, request, *args, **kwargs):
        return self._list(request, False, *args, **kwargs)

    def get_object_by_lookup_field(self, val):
        queryset = self.get_queryset()
        filter_kwargs = {self.lookup_field: val}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def get(self, request, *args, **kwargs):
        action = kwargs.pop("action", "")
        if action not in self.actions or request.method.lower() != self.action_method_map[action]:
            return self.http_method_not_allowed(request, *args, **kwargs)

        handler = getattr(self, action, None)
        if not handler:
            raise NotFound()
        return handler(request, *args, **kwargs)

    post = get

    @classmethod
    def register_to(cls, urlpatterns, base, name=None):
        # type: (List, str, Optional[str]) -> None
        urls = cls._scan_customed_methods()
        urlpatterns.append(
            url(base, include([url(path, handler, name=name) for path, handler, name in urls]))
        )

        actions = "|".join(cls.actions)
        pattern = url(
            urljoin(base, rf"(?P<action>{actions})$"),
            cls.as_view(actions=cls.actions, action_method_map=cls.action_method_map),
            name=name,
        )  # type: ignore
        urlpatterns.append(pattern)

    @classmethod
    def _scan_customed_methods(cls):
        urls = []
        for k, v in cls.__dict__.items():
            method = getattr(v, "method", "").lower()
            if not method:
                continue

            urls.append(
                (getattr(v, "url_path", k), cls._make_view_handler(k, [k], {k: method}), v.url_name)
            )
        return urls

    @classmethod
    def _make_view_handler(cls, action, actions, action_method_map):
        handler = cls.as_view(actions=actions, action_method_map=action_method_map)

        def wrapped(*args, **kwargs):
            return handler(*args, action=action, **kwargs)

        update_wrapper(wrapped, handler)
        return wrapped

    @classmethod
    def register_to_router(cls, router, base=""):
        # type: (Router, str) -> None
        if base:
            if not base.endswith("/"):
                base += "/"

        urls = cls._scan_customed_methods()
        for path, handler, name in urls:
            router.register(urljoin(base, path), handler, name)

        actions = "|".join(cls.actions)
        path = rf"(?P<action>{actions})$"
        path = urljoin(base, path)

        router.register(path, cls.as_view(actions=cls.actions, action_method_map=cls.action_method_map))


def new_simple_model_viewset(model_class, search_fields=None, actions=None):
    # type: (Type[Model], Optional[List[str]], Optional[List[str]]) -> Type[ModelViewSet]
    class AnonymousSerializer(ModelSerializer):
        class Meta:
            model = model_class
            fields = "__all__"

    _search_fields = search_fields if search_fields else []

    class AnoymousViewSet(ModelViewSet):
        queryset = model_class.objects.all()
        serializer_class = AnonymousSerializer
        search_fields = _search_fields

    if actions:
        AnoymousViewSet.actions = actions

    return AnoymousViewSet


def validate_serializer_data_safely(serializer):
    # type: (Serializer) -> None
    if serializer.is_valid():
        return

    errors = serializer.errors
    for field_name, error_details in errors.items():
        field = serializer.fields[field_name]
        logger.warning(f"validate field `{field.label}` is failed, {error_details}")
        for error_detail in error_details:
            try:
                message = ParseErrorCode.of(error_detail.code).to_message(field.label)
            except ValueError:
                message = f"field `{field.label}` has unexpected error `{str(error_detail)}`"

            raise BadRequest(message=message)
