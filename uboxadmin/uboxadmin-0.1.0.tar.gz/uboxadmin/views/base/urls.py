from django.conf.urls import include, url

from . import comm, open
from .sys import urls

urlpatterns = [
    url("^comm/", include(comm.router.urls)),
    url("^open/", include(open.router.urls)),
    url("^sys/", include(urls)),
]
