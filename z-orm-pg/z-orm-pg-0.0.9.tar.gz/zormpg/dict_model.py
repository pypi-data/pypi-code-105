from __future__ import annotations
from typing import Any, Dict, Iterable
from zormpg.base import DataModel
import peewee as pee
import json
import logging
logger = logging.getLogger(__name__)


class DictValue:

    def __init__(self, default) -> None:
        """
        default: default value
        the type of default value must be in str, int, float, bool, list, dict
        """
        self.default = default
        t = type(self.default)
        if t not in [str, int, float, bool, list, dict]:
            raise Exception(f'默认值类型必须在str, int, float, bool, list, dict中,但获得的是{t}')
        self.key = None
        self.owner: DictModel = None
        self.cache = None

    def _get_row(self) -> DictModel:
        return self.owner.select().where(self.owner.__class__._model_key == self.key).get()

    def _get(self):
        if self.cache is not None:
            return self.cache
        v = self.default
        n = self._count()
        if n == 0:
            return self.default
        try:
            v = self._get_row()._model_value
            self.cache = json.loads(v)
            return self.cache
        except:
            logger.warning(f'表{self.owner._table_name}的键{self.key}的值{v}解析失败.返回原始值')
            return v

    def _count(self):
        return self.owner.select().where(self.owner.__class__._model_key == self.key).count()

    def _set(self, value):
        if self._count() == 0:
            row = self.owner.__class__()
            row._model_key = self.key
        else:
            row = self._get_row()
        row._model_value = json.dumps(value)
        row.save()
        self.cache = value
        logger.debug(f'设置表 {self.owner._table_name} 的 {self.key} 为 {value}')


class DictModel(DataModel):

    _model_key = pee.CharField()
    _model_value = pee.TextField()

    def __init__(self, *args, **kwargs):
        self._stored_dict: Dict[str, DictValue] = {}
        for k, v in self.__class__.__dict__.items():
            if isinstance(v, DictValue):
                v.key = k
                v.owner = self
                self._stored_dict[k] = v
        super().__init__(*args, **kwargs)

    def __getattribute__(self, _name: str) -> Any:
        if _name == '_stored_dict':
            return super().__getattribute__(_name)
        if _name in self._stored_dict:
            return self._stored_dict[_name]._get()
        return super().__getattribute__(_name)

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == '_stored_dict':
            return super().__setattr__(__name, __value)
        if __name in self._stored_dict:
            return self._stored_dict[__name]._set(__value)
        else:
            return super().__setattr__(__name, __value)
