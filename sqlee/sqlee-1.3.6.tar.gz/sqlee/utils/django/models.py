#coding: utf-8
import os
import json
import requests
from sqlee.utils.backend import SqleeTable

if 'DJANGO_SETTINGS_MODULE' in os.environ:
    settings = __import__(os.environ['DJANGO_SETTINGS_MODULE']).settings
else:
    raise ImportError("Django工程未被执行，请在Django工程中导入Sqlee的Django组件.")
try:
    if not settings.ENABLE_SQLEE or settings.SQLEE_NAME.replace(" ", "") == "":
        raise ImportError('Sqlee未在Django被正确配置.')
except Exception as exc:
    raise ImportError('Sqlee未在Django被正确配置.') from exc

class URL:
    url = "https://gitee.com/"
    def __init__(self, url=None):
        self.url = url if url != None else self.url
        self.url = self.url if self.url[-1] == "/" else self.url + "/"
        
    def __add__(self, value):
        value = str(value)
        value = value if value[-1] == "/" else value + "/"
        return URL(url=self.url + value)
        
    def __truediv__(self, value):
        value = str(value)
        value = value if value[-1] == "/" else value + "/"
        return URL(url=self.url + value)

    def __str__(self):
        return self.url

class django_table_objects:
    def __init__(self, obj=None):
        self.obj = obj

    def all(self):
        return self.obj.columns
    
    def get(self, *args, **kwargs):
        need = len(kwargs)
        result = []
        for column in self.obj.columns:
            transit = 0
            for kwarg in kwargs:
                if kwargs[kwarg] in column.data:
                    transit += 1
            if transit == need:
                result.append(column)
        if len(result) != 1:
            raise ValueError("未找到或找到了多个匹配的数据，如果你试图筛选多数据，请参考‘filter’.")
        return result[0]

    def create(self, *args, **kwargs):
        column = self.obj.repo.list_folder(path=self.obj.name, int=True)
        if len(column) == 0:
            column = 0
        else:
            column = max(column) + 1
        self.obj.repo.make_folder(path=URL(self.obj.name)/column)

        datas = []
        for name in self.obj.namespace:
            if name == "id":
                continue

            if name in kwargs:
                datas.append(kwargs[name])
            else:
                datas.append(None)

        for i in range(len(datas)):
            self.obj.repo.upload_file(
                path = URL(self.obj.name) / column / i,
                content = json.dumps({"content": datas[i]})
                )
        self.obj.sync()
        return self.obj.columns

    def delete(self):
        self.obj.delete()
    
    @property
    def length(self):
        return len(self.obj.columns)

    def count(self):
        return len(self.obj.columns)
    
    def filter(self, *args, **kwargs):
        need = len(kwargs)
        result = []
        for column in self.obj.columns:
            transit = 0
            for kwarg in kwargs:
                if kwargs[kwarg] in column.data:
                    transit += 1
            if transit == need:
                result.append(column)
        return result

class ForeignKey:
    def __init__(self, model=None, id=None):
        self._repo = settings.SQLEE
        self._model = model
        self._id = id
        self.self._repo.objects.get(name=self._model).objects.get(id=self._id)

class Model:
    def __init__(self):
        self.repo = settings.SQLEE.repo
        self.tablename = "%s_%s" % (
            self.app,
            self.__class__.__name__
            )
        try:
            self.table = SqleeTable(name=self.tablename, repo=self.repo)
            self.objects = django_table_objects(obj=self.table)
        except Exception:
            pass