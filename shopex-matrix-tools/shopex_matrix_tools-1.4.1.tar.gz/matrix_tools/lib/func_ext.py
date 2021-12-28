#!/usr/bin/python
# -*- coding: UTF-8 -*-
# requests 中文文档 https://docs.python-requests.org/zh_CN/latest/user/advanced.html#blocking-or-nonblocking

import requests
import time
from requests import adapters

requests.adapters.DEFAULT_RETRIES = 3  # 默认超时重连次数, requests可以对同一个host保持长连接
requests.adapters.DEFAULT_POOLSIZE = 30  # 默认连接池大小（协程数尽量不要超过此大小）
requests.adapters.DEFAULT_POOLBLOCK = True  # 当超过限制时，由pool_block参数决定是否阻塞等待。


def shopex_request(url, req_type='post', data='', **kwargs):
    try:
        if req_type == 'post':
            if type(data) == str:  # json格式提交请求
                r = requests.post(url, json=data, **kwargs)
            if type(data) == dict:  # 表单格式提交请求
                r = requests.post(url, data=data, **kwargs)
        elif req_type == 'get':
            r = requests.get(url, **kwargs)
        else:
            r = requests.post(url, data=data)
        r.raise_for_status()
        return 'succ', r.text
    except requests.exceptions.HTTPError as e:
        write_log("{}_{}".format(url, str(e)), method=kwargs.get('sys_log_tag', 'matrix'))
        if r.status_code >= 500:
            return 'fail', str(e)
        return 'dams', str(e)
    except requests.exceptions.ConnectTimeout as e:
        write_log("{}_{}".format(url, str(e)), method=kwargs.get('sys_log_tag', 'matrix'))
        return 'fail', str(e)
    except Exception as e:
        write_log("{}_{}".format(url, str(e)), method=kwargs.get('sys_log_tag', 'matrix'))
        return 'fail', str(e)


def write_log(msg, method):
    import syslog
    syslog.openlog(method, syslog.LOG_LOCAL0)
    syslog.syslog(syslog.LOG_INFO, msg)


def str2sec(src_str, format='%Y-%m-%d %H:%M:%S', float_num=False):
    try:
        time_tuple = time.strptime(src_str, format)
        timestamp = time.mktime(time_tuple)
        return float_num and timestamp or int(timestamp)
    except Exception as e:
        return ''


def sec2str(format='%Y-%m-%d %H:%M:%S', sec=None, gmtime=False):
    try:
        func = time.gmtime if gmtime else time.localtime
        return time.strftime(format, func(sec))
    except Exception as e:
        return ''
