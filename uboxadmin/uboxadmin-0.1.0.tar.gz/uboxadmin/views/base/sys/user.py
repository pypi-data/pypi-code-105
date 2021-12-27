from uboxadmin.generic import ModelViewSet, Router, validate_serializer_data_safely
from uboxadmin.models.system import User
from uboxadmin.serializers import MoveUsersRequest, UserSerializer

router = Router()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    search_fields = ["username", "name", "nick_name", "remark"]
    serializer_class = UserSerializer


UserViewSet.register_to_router(router)


@router.post("move")
def move(request):
    serializer = MoveUsersRequest(data=request.data)
    validate_serializer_data_safely(serializer)
    data = serializer.validated_data
    User.objects.filter(id__in=data["user_ids"]).update(department_id=data["department_id"])
