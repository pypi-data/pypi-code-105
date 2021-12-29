from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Max, Value, Func, F, Case, When, Q
from rest_framework import viewsets
from rest_framework.response import Response

from vtb_django_utils.model_versions.utils.consts import REL_VERSION_CALCULATED_FIELD_END, VERSION_DELIMITER, \
    REL_VERSION_FIELD_END, REL_VERSION_PATTERN_FIELD_END
from vtb_django_utils.model_versions.utils.models import get_rel_model_version_str_from_dict, \
    get_rel_versioned_field_names
from vtb_django_utils.utils.db import get_model_fields


def get_version_str_func(rel_field_name=''):
    """ Преобразовывает массив с версией в строку """
    field_prefix = f'{rel_field_name}__' if rel_field_name else ''
    return Func(F(f'{field_prefix}versions__version_arr'), Value(VERSION_DELIMITER), function='array_to_string')


class VersionInfoMixin(viewsets.ModelViewSet):
    """ Миксин вьюсета версионных моделей с информацией о версиях """
    def get_queryset(self):
        # версии основной модели
        queryset = super().get_queryset().filter(versions__version_arr__isnull=False).annotate(
            last_version_query=Max(get_version_str_func()),
            version_list_query=ArrayAgg(get_version_str_func(), distinct=True),
        )

        # связанные версионные модели - Graph
        if rel_versioned_fields := get_rel_versioned_field_names(queryset.model):
            annotade_fields = {}
            for rel_field in rel_versioned_fields:
                # version str
                annotade_fields[f'{rel_field}{REL_VERSION_FIELD_END}_query'] = Case(
                    When(
                        Q(**{f'{rel_field}{REL_VERSION_FIELD_END}__isnull': False}),
                        then=Func(F(f'{rel_field}_version__version_arr'), Value(VERSION_DELIMITER),
                                  function='array_to_string')
                    )
                )

                # calculated version
                annotade_fields[f'{rel_field}{REL_VERSION_CALCULATED_FIELD_END}_query'] = Case(
                    # last_version
                    When(
                        Q(
                            Q(**{f'{rel_field}{REL_VERSION_PATTERN_FIELD_END}__isnull': True}) |
                            Q(**{f'{rel_field}{REL_VERSION_PATTERN_FIELD_END}': ''}),
                            **{
                                f'{rel_field}{REL_VERSION_FIELD_END}__isnull': True,
                            },
                        ),
                        then=Func(Max(f'{rel_field}__versions__version_arr'), Value(VERSION_DELIMITER), 
                                  function='array_to_string')
                    ),
                    # exact version
                    When(
                        **{f'{rel_field}{REL_VERSION_FIELD_END}__isnull': False},
                        then=Func(F(f'{rel_field}_version__version_arr'), Value(VERSION_DELIMITER), 
                                  function='array_to_string')
                    ),
                    # TODO - version pattern
                )
            queryset = queryset.annotate(**annotade_fields)
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
        instance_json['version_list'] = instance.version_list_query
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
