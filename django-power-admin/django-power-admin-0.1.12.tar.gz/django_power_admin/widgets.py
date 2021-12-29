from django.forms.widgets import PasswordInput
from django.forms.widgets import Select
from django.forms.widgets import SelectMultiple
from django.utils.translation import get_language

from django.contrib.admin.widgets import SELECT2_TRANSLATIONS

SELECT2_LANGUAGE_CODE = SELECT2_TRANSLATIONS.get(get_language())
SELECT2_I18N_FILES = []
if SELECT2_LANGUAGE_CODE:
    SELECT2_I18N_FILES += [
        "admin/js/vendor/select2/i18n/%s.js" % SELECT2_LANGUAGE_CODE
    ]

class Select2(Select):

    def __init__(self, attrs=None, choices=None):
        attrs = attrs or {}
        choices = choices or []
        if "class" in attrs:
            attrs["class"] += " django_power_admin_select2_widget"
        else:
            attrs["class"] = "django_power_admin_select2_widget"
        super().__init__(attrs=attrs, choices=choices)

    class Media:
        js=[
            "admin/js/vendor/jquery/jquery.js",
            "admin/js/vendor/select2/select2.full.js",
            "django_power_admin/widgets/Select2/js/Select2.js",
        ] + SELECT2_I18N_FILES + [
            "admin/js/jquery.init.js",
        ]
        css ={
            "all": [
                "admin/css/vendor/select2/select2.css",
            ]
        }

class SelectMultiple2(SelectMultiple):
    def __init__(self, attrs=None, choices=None):
        attrs = attrs or {}
        choices = choices or []
        if "class" in attrs:
            attrs["class"] += " django_power_admin_select2_multiple_widget"
        else:
            attrs["class"] = "django_power_admin_select2_multiple_widget"
        super().__init__(attrs=attrs, choices=choices)

    class Media:
        js=[
            "admin/js/vendor/jquery/jquery.js",
            "admin/js/vendor/select2/select2.full.js",
            "django_power_admin/widgets/SelectMultiple2/js/SelectMultiple2.js",
        ] + SELECT2_I18N_FILES + [
            "admin/js/jquery.init.js",
        ]
        css ={
            "all": [
                "admin/css/vendor/select2/select2.css",
            ]
        }

class PasswordResetableWidget(PasswordInput):
    pass
