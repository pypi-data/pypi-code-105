#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
服务端
"""

import socket               # 导入 socket 模块

from .constants import Constants
from .models import SocketRequest
from .models import SocketResponse
from .models import Socket
from .loggers import get_logger

__all__ = [
    'SocketClient',
    'stop_server',
    'send_message',
]

class SocketClient(Socket):
    logger = get_logger('Client')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.socket = socket.socket()

    def connect(self):
        """链接 socket 服务"""
        self.socket.connect( (self.host, self.port))

    def send(self, message):
        """发送消息"""
        if not isinstance(message, SocketRequest):
            message = SocketRequest(message = message)
        self.socket.send(message.dumps())
        res = self.receive_message()
        return res

    def stop_server(self):
        """停止服务"""
        data = SocketRequest().build_stop()
        return self.send(data)

    def close(self):
        self.socket.close()

    def receive_message(self):
        """接收消息"""
        data = b''
        while True:
            fragment = self.socket.recv(Constants.FRAGMENT_SIZE)
            if not fragment:
                break
            data += fragment
        #  self.logger.debug('接收服务端信息 %s', data)
        res = SocketResponse.loads(data)
        self.logger.debug('接收服务端信息 %s', res.to_dict())
        return res

def stop_server(host=None, port=None):
    """停止服务"""
    client = SocketClient(host = host, port = port)
    try:
        client.connect()
        client.stop_server()
        client.close()
    except ConnectionRefusedError:
        client.logger.debug('服务停止')

def send_message(message, host=None, port=None):
    client = SocketClient(host = host, port = port)
    try:
        client.connect()
        client.send(message)
        client.close()
    except ConnectionRefusedError:
        client.logger.debug('服务未启动')

if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    action = args[0]
    if action == 'stop_server':
        stop_server()
    else:
        send_message('test')
