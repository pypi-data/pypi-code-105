from django.conf.urls import include, url

from uboxadmin.generic import ModelViewSet
from uboxadmin.models.system import Menu
from uboxadmin.serializers import MenuSerializer

from . import department, log, param, role, user

urlpatterns = [
    url("^department/", include(department.router.urls)),
    url("^log/", include(log.router.urls)),
    url("^param/", include(param.router.urls)),
    url("^role/", include(role.router.urls)),
    url("^user/", include(user.router.urls)),
]


class MenuViewSet(ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


MenuViewSet.register_to(urlpatterns, "^menu/")
