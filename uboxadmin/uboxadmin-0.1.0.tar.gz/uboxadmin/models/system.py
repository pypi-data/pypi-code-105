from datetime import datetime, timedelta
from typing import Optional

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models, transaction

from uboxadmin.defines import ParamType, UserStatus
from uboxadmin.models.base import BaseModel


class Conf(BaseModel):
    key = models.CharField("配置键", max_length=255, unique=True)
    value = models.CharField("配置值", max_length=255)

    @classmethod
    def get_value(cls, key):
        # type: (str) -> Optional[str]
        try:
            return cls.objects.get(key=key).value
        except cls.DoesNotExist:
            return None

    @classmethod
    def update_value(cls, key, val):
        # type: (str, str) -> None
        cls.objects.update_or_create({"value": val, "key": key}, key=key)


class Department(BaseModel):
    name = models.CharField("部门名称", max_length=255)
    parent_id = models.IntegerField("上级部门ID", null=True)
    order_num = models.IntegerField("排序", default=0)


class Log(BaseModel):
    user_id = models.BigIntegerField("用户ID", db_index=True, null=True)
    action = models.CharField("行为", max_length=100)
    ip = models.GenericIPAddressField("ip", null=True)
    ip_addr = models.CharField("ip地址", max_length=50, null=True)
    params = models.TextField("参数", null=True)

    @classmethod
    def clear(cls, all=False):
        if all:
            cls.objects.all().delete()
            return

        keep_day = Conf.get_value("logKeep")
        if not keep_day:
            cls.objects.all().delete()
            return

        before = datetime.now() - timedelta(days=float(keep_day))
        cls.objects.filter(create_time__lt=before)

    @classmethod
    def record(cls, ip, url, params, user_id):
        # type: (str, str, str, str) -> None
        cls.objects.create(ip=ip, action=url, params=params, user_id=user_id)


class Menu(BaseModel):
    parent_id = models.IntegerField("上级部门ID", null=True)
    name = models.CharField("菜单名称", max_length=255)
    router = models.CharField("菜单地址", null=True, max_length=255)
    perms = models.CharField("权限标识", null=True, max_length=255)
    type = models.IntegerField("类型", default=0, help_text="类型 0：目录 1：菜单 2：按钮")
    icon = models.CharField("图标", max_length=255, null=True)
    order_num = models.IntegerField("排序", default=0)
    view_path = models.CharField("视图地址", null=True, max_length=255)
    keep_alive = models.BooleanField("路由缓存", default=True)
    is_show = models.BooleanField("是否展示", default=True)


class Param(BaseModel):
    key_name = models.CharField("键位", max_length=255, db_index=True, help_text="键位")
    name = models.CharField("名称", max_length=255)
    data = models.TextField("数据")
    data_type = models.IntegerField(
        "数据类型",
        default=0,
        help_text="数据类型 0:字符串 1：数组 2：键值对",
        choices=ParamType.as_choices(),
    )
    remark = models.CharField("备注", max_length=255, null=True)


class Role(BaseModel):
    user_id = models.CharField("用户ID", max_length=255)
    name = models.CharField("名称", max_length=255, unique=True)
    label = models.CharField("角色标签", max_length=255, null=True, unique=True, db_index=True)
    remark = models.CharField("备注", max_length=255, null=True)
    relevance = models.IntegerField("数据权限是否关联上下级", default=1)

    @property
    def department_ids(self):
        return [rd.department_id for rd in RoleDepartment.objects.filter(role_id=self.pk)]

    @department_ids.setter
    def department_ids(self, ids):
        with transaction.atomic():
            RoleDepartment.objects.filter(role_id=self.pk).delete()
            for id_ in ids:
                RoleDepartment.objects.update_or_create(role_id=self.pk, department_id=id_)

    @property
    def menu_ids(self):
        return [rm.menu_id for rm in RoleMenu.objects.filter(role_id=self.pk)]

    @menu_ids.setter
    def menu_ids(self, ids):
        with transaction.atomic():
            RoleMenu.objects.filter(role_id=self.pk).delete()
            for id_ in ids:
                RoleMenu.objects.update_or_create(role_id=self.pk, menu_id=id_)


class RoleDepartment(BaseModel):
    role_id = models.IntegerField("角色ID")
    department_id = models.IntegerField("部门ID")


class RoleMenu(BaseModel):
    role_id = models.IntegerField("角色ID")
    menu_id = models.IntegerField("菜单ID")


class User(BaseModel, AbstractBaseUser):
    department_id = models.IntegerField("部门ID", null=True, db_index=True)
    name = models.CharField("姓名", null=True, max_length=255)
    username = models.CharField("用户名", unique=True, max_length=255)
    password = models.CharField("密码", max_length=255)
    password_v = models.IntegerField("密码版本", default=1, help_text="作用是改完密码，让原来的token失效")
    nick_name = models.CharField("昵称", null=True, max_length=255)
    head_img = models.CharField("头像", null=True, max_length=255)
    phone = models.CharField("手机", db_index=True, max_length=20, null=True)
    email = models.EmailField("邮箱", null=True)
    remark = models.CharField("备注", null=True, max_length=255)
    status = models.IntegerField("状态", default=1, choices=UserStatus.as_choices())
    # department_name: str
    # role_id_list: List[int]

    USERNAME_FIELD = "username"

    def save(self, *args, **kwargs) -> None:
        if not self.password:
            self.set_password("123456")

        return super(AbstractBaseUser, self).save(*args, **kwargs)

    @property
    def department(self):
        if self.department_id is None:
            return None

        return Department.objects.get(id=self.department_id)

    @property
    def role_name(self):
        role_ids = self.role_ids
        roles = map(lambda id: Role.objects.get(id=id), role_ids)
        role_names = map(lambda role: role.name, roles)
        result = ",".join(name for name in role_names)
        return result

    @property
    def STATUS(self):
        return UserStatus(self.status)

    @property
    def role_ids(self):
        user_roles = UserRole.objects.filter(user_id=self.pk)
        return [ur.role_id for ur in user_roles]

    @role_ids.setter
    def role_ids(self, ids):
        with transaction.atomic():
            UserRole.objects.filter(user_id=self.pk).delete()
            for id_ in ids:
                UserRole.objects.update_or_create(user_id=self.pk, role_id=id_)

    @property
    def menus(self):
        if self.is_admin():
            # TODO: GROUP BY Menu.id
            return Menu.objects.all().order_by("order_num")
        else:
            menu_ids = RoleMenu.objects.filter(role_id__in=self.role_ids).values_list("menu_id", flat=True)
            return Menu.objects.filter(id__in=menu_ids).order_by("order_num")

    def is_admin(self):
        return self.username == "admin"

    @property
    def permissions(self):
        role_ids = self.role_ids
        if not role_ids:
            return []

        if 1 in role_ids:
            # user is admin
            queryset = Menu.objects.filter(~models.Q(perms=None))
        else:
            menu_ids = RoleMenu.objects.filter(role_id__in=role_ids).values_list("menu_id", flat=True)
            queryset = Menu.objects.filter(~models.Q(perms=None), id__in=menu_ids)

        return tuple(set(queryset.values_list("perms", flat=True)))


class UserRole(BaseModel):
    user_id = models.IntegerField("用户ID")
    role_id = models.IntegerField("角色ID")
