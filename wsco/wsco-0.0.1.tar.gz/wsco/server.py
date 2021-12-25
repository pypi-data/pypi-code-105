#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
服务端
"""

import socket               # 导入 socket 模块
import traceback

from .constants import Constants
from .exceptions import ServerStopException
from .models import (
    Socket,
    SocketRequest,
    SocketResponse,
)
from .message_handler import (
    MessageHandler,
    MessageReturn,
)
from .loggers import get_logger

from threading import Event

done_event = Event()

def handle_sigint(signum, frame):
    done_event.set()

import signal
signal.signal(signal.SIGINT, handle_sigint)

__all__ = ['SocketServer']

class SocketServer(Socket):
    logger = get_logger('Server')

    def __init__(self, message_handler: MessageHandler = MessageReturn(),
            **kwargs):
        super().__init__(**kwargs)
        self.socket = socket.socket()
        self.message_handler = message_handler

    def run(self):
        """运行服务
        """
        self.logger.debug(f"开始运行服务，地址: {self.host}:{self.port}")
        # 处理 TCP 断开后端口占用问题
        # https://blog.csdn.net/Jason_WangYing/article/details/105420659
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)

        while True:
            if done_event.is_set():
                self.logger.debug('服务停止')
                break
            try:
                self.accept()
            except ServerStopException:
                self.logger.debug('服务停止')
                break

    def accept(self):
        """接收客户端信息"""
        c,addr = self.socket.accept()     # 建立客户端连接
        self._accept(c)
        c.close()                # 关闭连接

    def _accept(self, socket):
        """接收客户端信息"""
        req = self.receive_message(socket)
        #  if req.is_unkown():
            #  socket.send(SocketResponse.build_unkown().dumps())
            #  return

        if req.is_stop():
            socket.send(SocketResponse(data = 'server stop').dumps())
            raise ServerStopException()

        try:
            res = self.message_handler.handle(req)
            sres = SocketResponse(data=res)
        except Exception as e:
            self.logger.error(traceback.format_exc())
            self.logger.error(traceback.format_stack())
            sres = SocketResponse(code = 1, data=str(e))
        socket.send(sres.dumps())

    def receive_message(self, receive_socket: socket.socket):
        """接收消息"""
        data = receive_socket.recv(Constants.FRAGMENT_SIZE)
        req = SocketRequest.loads(data)
        self.logger.debug('接收客户端消息 {}'.format(req.to_dict()))
        return req

if __name__ == "__main__":
    SocketServer().run()
