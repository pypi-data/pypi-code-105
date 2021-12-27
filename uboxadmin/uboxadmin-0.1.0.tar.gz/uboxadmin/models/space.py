from django.db import models

from uboxadmin.models.base import BaseModel


# 文件信息管理
class AppSpaceInfo(BaseModel):
    url = models.CharField("地址", max_length=255)
    type = models.CharField("类型", max_length=255)
    classify_id = models.IntegerField("分类ID", null=True)


# 图片空间信息分类
class AppSpaceType(BaseModel):
    name = models.CharField("类别名称", max_length=255)
    parent_id = models.IntegerField("父类型ID", null=True)
