from uboxadmin.generic import ModelViewSet, Router, validate_serializer_data_safely
from uboxadmin.models.system import Conf, Log
from uboxadmin.serializers import LogSerializer, SetLogKeepRequest

router = Router()


class LogViewSet(ModelViewSet):
    actions = ["page"]
    serializer_class = LogSerializer
    queryset = Log.objects.all().extra(
        select={"name": "uboxadmin_user.name"},
        tables=["uboxadmin_user"],
        where=["user_id = uboxadmin_user.id"],
    )


LogViewSet.register_to_router(router)


@router.post("clear")
def clear(request):
    Log.clear(True)


@router.post("setKeep")
def set_keep(request):
    serializer = SetLogKeepRequest(data=request.data)
    validate_serializer_data_safely(serializer)
    data = serializer.validated_data

    Conf.update_value("logKeep", data["value"])


@router.get("getKeep")
def get_keep(request):
    value = Conf.get_value("logKeep")
    return value
