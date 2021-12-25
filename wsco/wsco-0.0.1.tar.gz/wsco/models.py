#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
模型
"""

import abc
import pickle
import json

from wpy.base import BaseObject
from wpy.base import BaseEnum

from .constants import SocketConstants


class PickleModel(BaseObject):

    def dumps(self):
        '''序列化'''
        return pickle.dumps(self.to_dict())

    @classmethod
    def loads(cls, bytes_data):
        """加载"""
        data = pickle.loads(bytes_data)
        return cls(**data)


class SRAction(BaseEnum):
    MESSAGE = 'message'   # 消息
    STOP = 'stop'   # 停止服务


class SocketRequest(PickleModel):

    action = SRAction.MESSAGE.value
    message = None

    def is_stop(self):
        """是否为停止"""
        return self.action == SRAction.STOP.value

    #  def is_unkown(self):
        #  """是否不明确的信息"""
        #  return self.action not in SRAction.values()

    @classmethod
    def build_stop(cls):
        return cls(action = SRAction.STOP.value)


class SocketResponse(PickleModel):
    code = 0
    message = None

    def json(self):
        """将数据格式化为 dict 结构"""
        if isinstance(self.message, dict) or \
                isinstance(self.message, list):
            return self.message
        else:
            try:
                return json.loads(self.message)
            except:
                return None
        return None

    #  @classmethod
    #  def build_unkown(cls):
        #  """构建 unkown 回复"""
        #  return cls(code = 1, data='unkown message')

    @classmethod
    def build_error(cls, e):
        return cls(code = 1, message=e)

class Socket(object, metaclass=abc.ABCMeta):

    def __init__(self, host=None, port=None, logger = None, **kwargs):
        self.host = host or SocketConstants.HOST
        self.port = port or SocketConstants.PORT
        if logger:
            self.logger = logger
