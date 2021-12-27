from django.conf.urls import include, url

from .base import urls as base_urls
from .django_apps import router
from .space import urls as space_urls

urlpatterns = [
    url("^admin/base/", include(base_urls)),
    url("^admin/space/", include(space_urls)),
    url("^admin/django-apps/", include(router.urls))
]
