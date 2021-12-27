from uboxadmin.generic import ModelViewSet, Router
from uboxadmin.models.system import Param
from uboxadmin.serializers import ParamSerializer

router = Router()


class ParamViewSet(ModelViewSet):
    serializer_class = ParamSerializer
    queryset = Param.objects.all()
    actions = ["add", "delete", "update", "info", "page"]
    search_fields = ["key_name", "name", "remark"]


ParamViewSet.register_to_router(router)


@router.get("html")
def html_by_key(request):
    raise NotImplementedError
