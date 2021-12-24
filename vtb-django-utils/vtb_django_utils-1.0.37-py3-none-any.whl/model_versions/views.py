from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Max, Value, Func, F
from rest_framework import viewsets
from rest_framework.response import Response

from vtb_django_utils.model_versions.utils.consts import REL_VERSION_CALCULATED_FIELD_END, VERSION_DELIMITER
from vtb_django_utils.model_versions.utils.models import get_rel_model_version_str_from_dict
from vtb_django_utils.utils.db import get_model_fields


def get_version_str_func():
    """ Преобразовывает массив с версией в строку """
    return Func(F('versions__version_arr'), Value(VERSION_DELIMITER), function='array_to_string')


class VersionInfoMixin(viewsets.ModelViewSet):
    """ Миксин вьюсета версионных моделей с информацией о версиях """
    def get_queryset(self):
        queryset = super().get_queryset().filter(versions__version_arr__isnull=False).annotate(
            last_version_fast=Max(get_version_str_func()),
            version_list_fast=ArrayAgg(get_version_str_func()),
        )
        return queryset


class VersionMixin(viewsets.ModelViewSet):
    """ Миксин вьюсета версионных моделей """
    def _json_by_version(self, obj=None) -> dict:
        instance = obj or self.get_object()
        version = self.request.query_params.get('version')
        json_field_name = self.request.query_params.get('json_name', 'json')
        compare_with_version = self.request.query_params.get('compare_with_version')
        instance_json = instance.get_json_by_version(version, json_field_name, compare_with_version)
        # добавляем версии связанных моделей
        instance.add_version_for_rel_versioned_obj(instance_json)
        instance_json['version_list'] = instance.version_list
        return instance_json

    def retrieve(self, request, *args, **kwargs):
        return Response(self._json_by_version())


class VersionedRelMixin(viewsets.ModelViewSet):
    """ Миксин вьюсета моделей, у которых есть поля с версионными моделями """
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        instance = self.get_object()

        # добавляем рассчитанную версию версионной модели
        rel_fields = [f for f in get_model_fields(instance.__class__) if f.name in instance.rel_versioned_fields]
        for field in rel_fields:
            calc_field = f'{field.name}{REL_VERSION_CALCULATED_FIELD_END}'
            response.data[calc_field] = get_rel_model_version_str_from_dict(response.data, field)
        return response
