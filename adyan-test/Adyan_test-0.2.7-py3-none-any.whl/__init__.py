#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/6 13:43
# @Author  : Adyan
# @File    : __init__.py.py
import time

from flask import Flask, request, g
from flask_cors import CORS
from gevent import monkey

# from .config_mongo import settings
# from .login.cookies import Cookies
#
# from .Utils import ReidsClient
# from .port_way import PortWay
# from .proxy.scheduler import Scheduler

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

from pipy_pkg.Adyan.port_way import PortWay

monkey.patch_all()
app = Flask(__name__)
app.config.update(
    DEBUG=True
)
CORS(app, supports_credentials=True)

way = PortWay


# cookies
@app.route('/cookie', methods=["post", "get"])
def cookie():
    # http://192.168.31.252:9090/cookie?type=MY_USER&host=47.107.86.234&login_url=https://m.tb.cn/h.fSL3oPQ?sm=051ba2&dbName=h5&DB=3
    return PortWay(request).cookie()


# ip pool
@app.route('/proxy', methods=["post", "get"])
def ip_pool():
    # http://192.168.31.252:9090/get?key=228923910&count=1000&HOST=47.107.86.234&PORT=27017
    return PortWay(request).ip_pool()


def start(host, prot):
    """9090"""
    app.run(host=host, port=prot)
    http_server = WSGIServer((host, prot), app, handler_class=WebSocketHandler)
    http_server.serve_forever()


start('0.0.0.0',9090)