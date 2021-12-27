from djangorestframework_camel_case.parser import CamelCaseFormParser, CamelCaseJSONParser, CamelCaseMultiPartParser
from djangorestframework_camel_case.render import CamelCaseBrowsableAPIRenderer, CamelCaseJSONRenderer
from rest_framework.settings import api_settings

from uboxadmin.settings import admin_settings


class APIViewConf:
    renderer_classes = [
        CamelCaseJSONRenderer,
        CamelCaseBrowsableAPIRenderer,
    ] + api_settings.DEFAULT_RENDERER_CLASSES  # type: ignore
    parser_classes = [
        CamelCaseFormParser,
        CamelCaseMultiPartParser,
        CamelCaseJSONParser,
    ] + api_settings.DEFAULT_PARSER_CLASSES  # type: ignore
    authentication_classes = admin_settings.DEFAULT_AUTHENTICATION_CLASSES
    permission_classes = admin_settings.DEFAULT_PERMISSION_CLASSES

    def get_exception_handler(self):
        return admin_settings.EXCEPTION_HANDLER
