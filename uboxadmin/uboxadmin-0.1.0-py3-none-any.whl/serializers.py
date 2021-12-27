from rest_framework.fields import CharField, DateTimeField, IntegerField, ListField
from rest_framework.serializers import ModelSerializer, Serializer

from uboxadmin.models.system import Department, Log, Menu, Param, Role, User


class CaptchaRequest(Serializer):
    type = CharField(required=False)
    width = IntegerField()
    height = IntegerField()


class PersonUpdateRequest(Serializer):
    nick_name = CharField(required=False)
    head_img = CharField(required=False)
    password = CharField(required=False)


class SetLogKeepRequest(Serializer):
    value = IntegerField()


class HtmlByKeyRequest(Serializer):
    key = CharField()


class MoveUsersRequest(Serializer):
    department_id = IntegerField()
    user_ids = ListField(child=IntegerField())


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class UpdateDepartmentOrderSerializer(Serializer):
    id = IntegerField()
    parent_id = IntegerField(allow_null=True)
    order_num = IntegerField()


class UpdateDepartmentOrderRequest(Serializer):
    data = ListField(child=UpdateDepartmentOrderSerializer())


class LogSerializer(ModelSerializer):
    name = CharField()

    class Meta:
        model = Log
        fields = "__all__"


class ParamSerializer(ModelSerializer):
    class Meta:
        model = Param
        fields = "__all__"


DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class BaseSerializer(ModelSerializer):
    create_time = DateTimeField(format=DATETIME_FORMAT, read_only=True)
    update_time = DateTimeField(format=DATETIME_FORMAT, read_only=True)


class UserSerializer(BaseSerializer):
    password = CharField(write_only=True, required=False)
    department_name = CharField(source="department.name", read_only=True)
    role_name = CharField(read_only=True)
    role_id_list = ListField(source="role_ids")

    def create(self, validated_data):
        role_ids = []
        if "role_ids" in validated_data:
            role_ids = validated_data.pop("role_ids")

        inst = super().create(validated_data)
        inst.role_ids = role_ids
        return inst

    def update(self, instance, validated_data):
        if "role_ids" in validated_data:
            instance.role_ids = validated_data.pop("role_ids")
        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = "__all__"


class RoleSerializer(BaseSerializer):
    menu_id_list = ListField(source="menu_ids")
    department_id_list = ListField(source="department_ids")

    def create(self, validated_data):
        menu_ids = []
        if "menu_ids" in validated_data:
            menu_ids = validated_data.pop("menu_ids")

        department_ids = []
        if "department_ids" in validated_data:
            department_ids = validated_data.pop("department_ids")

        inst = super().create(validated_data)
        inst.menu_ids = menu_ids
        inst.department_ids = department_ids
        return inst

    def update(self, instance, validated_data):
        if "menu_ids" in validated_data:
            instance.menu_ids = validated_data.pop("menu_ids")

        if "department_ids" in validated_data:
            instance.department_ids = validated_data.pop("department_ids")
        return super().update(instance, validated_data)

    class Meta:
        model = Role
        fields = "__all__"


class MenuSerializer(BaseSerializer):
    class Meta:
        model = Menu
        fields = "__all__"
