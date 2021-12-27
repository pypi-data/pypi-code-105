from django.db.models.query_utils import Q

from uboxadmin.generic import ModelViewSet, Router
from uboxadmin.models.system import Role
from uboxadmin.serializers import RoleSerializer

router = Router()


class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    search_fields = ["name", "label", "remark"]

    def get_queryset(self):
        user = self.request.user
        query = ~Q(label="admin") and (Q(user_id=user.id) or Q(id__in=user.role_ids))
        return super().get_queryset().filter(query)

    def add(self, request, *args, **kwargs):
        request.data["user_id"] = self.request.user.id
        return super().add(request, *args, **kwargs)


RoleViewSet.register_to_router(router)
