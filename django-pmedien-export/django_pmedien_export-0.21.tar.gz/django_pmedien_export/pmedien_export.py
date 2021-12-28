# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.apps import apps
from django.http import HttpResponse

# Create your views here.

from django.conf import settings

"""
import in urls like this:

from django_pmedien_export import export

urlpatterns = [
...
url(r'^export/((?P<appname>[\w-]+)/)?$', export.export),
...
]

also set LANGUAGES in settings.py like:

LANGUAGES = (
    ('de', 'deutsch'),
)
"""


def get_translations(obj, field):
    if hasattr(settings, 'LANGUAGES') and len(settings.LANGUAGES):
        return {
            lang[0]: getattr(obj, '{}_{}'.format(field, lang[0]))
            if getattr(obj, '{}_{}'.format(field, lang[0]), None)
            else getattr(obj, '{}'.format(field))
            for lang in settings.LANGUAGES
        }
    else:
        return getattr(obj, field, None)


def return_value(obj, field, file_list):
    internal_type = field.get_internal_type()
    value = getattr(obj, field.name, None)
    if value is not None:
        if internal_type in ['DateField', 'DateTimeField', 'TimeField']:
            value = '{}'.format(value)
        elif internal_type in ['AutoField']:
            pass
        elif internal_type in ['DurationField']:
            value = value.total_seconds()
        elif internal_type in ['FileField', 'ImageField']:
            value = get_translations(obj, field.name)
            if hasattr(settings, 'LANGUAGES') and len(settings.LANGUAGES):
                value = {key: value[key].url for key in value if bool(value[key])}
                file_list.update(value.values())
            else:
                file_list.add(value)
        elif internal_type in ['ForeignKey', 'OneToOneField']:
            try:
                value = value.id
            except:
                value = None
        elif internal_type in ['ManyToManyField']:
            value = [x.id for x in value.all()]
        elif internal_type in ['CharField', 'TextField', 'SlugField']:
            value = get_translations(obj, field.name)
        elif internal_type in ['IntegerField', 'PositiveIntegerField', 'BooleanField', 'FloatField']:
            pass
        elif internal_type in ['TreeForeignKey']:
            if hasattr(value, 'values_list'):
                value = [x['id'] for x in value.values()]
            if hasattr(value, 'parent_id'):
                value = 'inconsistent by mptt.'
        else:
            value = 'Don\'t know this data-type: {}'.format(internal_type)
    else:
        if field.is_relation and field.auto_created:
            value = getattr(obj, field.get_accessor_name(), None)
            if value:
                value = [x.id for x in value.all()]
    return value


def serialize_entry(obj, file_list):
    serialized = {
        line.name: return_value(obj, line, file_list) for line in obj._meta.get_fields() if
        not hasattr(line, 'language')  # we dont wnat references to translated fields
    }
    return serialized


def export(request, appname, *args):
    models = {}
    file_list = set()
    if apps.is_installed(appname):
        app = apps.get_app_config(appname)
        app_models = app.get_models()

        for model in app_models:
            models.setdefault(model._meta.model_name, {})
            my_entry = {
                entry.id: serialize_entry(entry, file_list) for entry in model.objects.all()
            }
            models[model._meta.model_name] = my_entry

    try:
        return HttpResponse(
            json.dumps(
                {'data': models, 'files': list(file_list)},
                indent=4
            ),
            content_type='application/json'
        )
    except:
        return HttpResponse(json.dumps({'error': 'while serialization.'}), content_type='application/json')
