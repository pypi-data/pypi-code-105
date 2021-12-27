import re
from typing import Type

from django.core.exceptions import FieldDoesNotExist
from django.db.models import Model
from django.db.models.query import QuerySet
from rest_framework.filters import BaseFilterBackend, SearchFilter as _SearchFilter
from rest_framework.request import Request

from uboxadmin.settings import admin_settings


class OrderingFilter(BaseFilterBackend):
    sorting_keywords = {"desc": "-", "asc": ""}
    pattern = re.compile(r"(?<!^)(?=[A-Z])")

    def filter_queryset(self, request, queryset, view):
        """
        Return a filtered queryset.
        """
        order = request.data.get("order", view.ordering_field)
        order = self.pattern.sub("_", order).lower()
        sort = request.data.get("sort", view.sorting)
        if sort not in self.sorting_keywords:
            sort = admin_settings.DEFAULT_SORTING

        mapped_keyword = self.sorting_keywords[sort]  # type: ignore
        return queryset.order_by(f"{mapped_keyword}{order}")


class SearchFilter(_SearchFilter):
    search_param = admin_settings.SEARCH_PARAM

    def get_search_terms(self, request):
        try:
            return [request.data[self.search_param]]
        except KeyError:
            return []


class ConditionFilter(BaseFilterBackend):
    control_keywords = {"size", "sort", "page", "order"}

    def filter_queryset(self, request, queryset, view):
        return self.filter_equals(request, self.filter_relations(request, queryset))

    def filter_relations(self, request, queryset):
        # type: (Request, QuerySet) -> QuerySet
        it = filter(lambda item: "ids" in item[0], request.data.items())  # type: ignore
        it = map(lambda item: (item[0].replace("ids", "id__in"), item[1]), it)
        return queryset.filter(**dict(it))

    def _test_field_name(self, model, field_name):
        # type: (Type[Model], str) -> bool
        try:
            model._meta.get_field(field_name)
            return True
        except FieldDoesNotExist:
            return False

    def filter_equals(self, request, queryset):
        # type: (Request, QuerySet) -> QuerySet
        model = queryset.model  # type: Type[Model]
        it = filter(lambda item: item[0] not in self.control_keywords, request.data.items())  # type: ignore
        it = filter(lambda item: self._test_field_name(model, item[0]), it)  # type: ignore
        return queryset.filter(**dict(it))
