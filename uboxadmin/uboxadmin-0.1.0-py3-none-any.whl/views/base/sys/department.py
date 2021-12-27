from uboxadmin.generic import ModelViewSet, Router, validate_serializer_data_safely
from uboxadmin.models.system import Department
from uboxadmin.serializers import DepartmentSerializer, UpdateDepartmentOrderRequest

router = Router()


class DepartmentViewSet(ModelViewSet):
    serializer_class = DepartmentSerializer
    actions = ["add", "delete", "update", "list"]
    queryset = Department.objects.all()
    search_fields = ["name"]


DepartmentViewSet.register_to_router(router)


@router.post("order")
def order(request):
    data = request.data
    serializer = UpdateDepartmentOrderRequest(data={"data": data})
    validate_serializer_data_safely(serializer)
    data = serializer.data["data"]

    for entity in data:
        department = Department.objects.get(id=entity["id"])
        department.__dict__.update(entity)
        department.save()
