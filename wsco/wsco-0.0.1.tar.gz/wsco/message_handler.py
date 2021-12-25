#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
消息处理器
"""

import abc

from .models import SocketRequest

class MessageHandler(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def handle(self, request: SocketRequest):
        """socket 消息处理方法"""
        pass


class MessageReturn(MessageHandler):
    """消息直接返回"""

    def handle(self, request: SocketRequest):
        """直接返回消息"""
        return request.message
