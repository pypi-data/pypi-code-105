from django.conf.urls import include, url

from uboxadmin.views import urls

urlpatterns = [
    url("^api/", include(urls)),
]
