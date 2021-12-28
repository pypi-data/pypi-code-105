import json
import socket
import os
import re

import threading
import asyncio

from asyncio.base_events import Server
from concurrent.futures import ThreadPoolExecutor
from asyncio.streams import StreamReader, StreamWriter
from ssl import PROTOCOL_TLS_SERVER, SSLContext
from collections import OrderedDict
from socketserver import TCPServer
from time import sleep
from urllib.parse import unquote

from typing import Any, Callable, Dict, List, Tuple

from simple_schedule import TaskFunction, StaticFile
from .http_protocol_handler import HttpProtocolHandler, SocketServerStreamRequestHandlerWraper

from .__utils import remove_url_first_slash, get_function_args, get_function_kwargs, get_path_reg_pattern
from .logger import get_logger

_logger = get_logger("simple_schedule.http_server")


class RoutingConf:

    HTTP_METHODS = [ "GET", "POST"]

    def __init__(self, res_conf={}):
        self.method_url_mapping: Dict[str,
                                      Dict[str, TaskFunction]] = {"_": {}}
        self.path_val_url_mapping: Dict[str, Dict[str, TaskFunction]] = {
            "_": OrderedDict()}
        self.method_regexp_mapping: Dict[str, Dict[str, TaskFunction]] = {
            "_": OrderedDict()}
        for mth in self.HTTP_METHODS:
            self.method_url_mapping[mth] = {}
            self.path_val_url_mapping[mth] = OrderedDict()
            self.method_regexp_mapping[mth] = OrderedDict()

        self.filter_mapping = OrderedDict()
        self._res_conf = []
        self.add_res_conf(res_conf)

        self.error_page_mapping = {}

    @property
    def res_conf(self):
        return self._res_conf

    @res_conf.setter
    def res_conf(self, val: Dict[str, str]):
        self._res_conf.clear()
        self.add_res_conf(val)

    def add_res_conf(self, val: Dict[str, str]):
        if not val or not isinstance(val, dict):
            return
        for res_k, v in val.items():
            if res_k.startswith("/"):
                k = res_k[1:]
            else:
                k = res_k
            if k.endswith("/*"):
                key = k[0:-1]
            elif k.endswith("/**"):
                key = k[0:-2]
            elif k.endswith("/"):
                key = k
            else:
                key = k + "/"

            if v.endswith(os.path.sep):
                val = v
            else:
                val = v + os.path.sep
            self._res_conf.append((key, val))
        self._res_conf.sort(key=lambda it: -len(it[0]))

    def map_controller(self, ctrl: TaskFunction):
        url = ctrl.url
        regexp = ctrl.regexp
        method = ctrl.method
        _logger.debug(
            f"map url {url}|{regexp} with method[{method}] to function {ctrl.func}. ")
        assert method is None or method == "" or method.upper() in self.HTTP_METHODS
        _method = method.upper() if method is not None and method != "" else "_"
        if regexp:
            self.method_regexp_mapping[_method][regexp] = ctrl
        else:
            _url = remove_url_first_slash(url)

            path_pattern, path_names = get_path_reg_pattern(_url)
            if path_pattern is None:
                self.method_url_mapping[_method][_url] = ctrl
            else:
                self.path_val_url_mapping[_method][path_pattern] = (
                    ctrl, path_names)

    def get_url_controller(self, path="", method="") -> Tuple[TaskFunction, Dict, List]:
        # explicitly url matching
        if path in self.method_url_mapping[method]:
            return self.method_url_mapping[method][path], {}, ()
        elif path in self.method_url_mapping["_"]:
            return self.method_url_mapping["_"][path], {}, ()

        # url with path value matching
        fun_and_val = self.__try_get_from_path_val(path, method)
        if fun_and_val is None:
            fun_and_val = self.__try_get_from_path_val(path, "_")
        if fun_and_val is not None:
            return fun_and_val[0], fun_and_val[1], ()

        # regexp
        func_and_groups = self.__try_get_from_regexp(path, method)
        if func_and_groups is None:
            func_and_groups = self.__try_get_from_regexp(path, "_")
        if func_and_groups is not None:
            return func_and_groups[0], {}, func_and_groups[1]
        # static files
        for k, v in self.res_conf:
            if path.startswith(k):
                def static_fun():
                    return self._res_(path, k, v)
                return TaskFunction(func=static_fun), {}, ()
        return None, {}, ()

    def __try_get_from_regexp(self, path, method):
        for regex, ctrl in self.method_regexp_mapping[method].items():
            m = re.match(regex, path)
            _logger.debug(
                f"regexp::pattern::[{regex}] => path::[{path}] match? {m is not None}")
            if m:
                return ctrl, tuple([unquote(v) for v in m.groups()])
        return None

    def __try_get_from_path_val(self, path, method):
        for patterns, val in self.path_val_url_mapping[method].items():
            m = re.match(patterns, path)
            _logger.debug(
                f"url with path value::pattern::[{patterns}] => path::[{path}] match? {m is not None}")
            if m:
                fun, path_names = val
                path_values = {}
                for idx in range(len(path_names)):
                    key = unquote(path_names[idx])
                    path_values[key] = unquote(m.groups()[idx])
                return fun, path_values
        return None


    def map_error_page(self, code: str, error_page_fun: Callable):
        if not code:
            c = "_"
        else:
            c = str(code).lower()
        self.error_page_mapping[c] = error_page_fun

    def _default_error_page(self, code: int, message: str = "", explain: str = ""):
        return json.dumps({
            "code": code,
            "message": message,
            "explain": explain
        })

    def error_page(self, code: int, message: str = "", explain: str = ""):
        c = str(code)
        func = None
        if c in self.error_page_mapping:
            func = self.error_page_mapping[c]
        elif code > 200:
            c0x = c[0:2] + "x"
            if c0x in self.error_page_mapping:
                func = self.error_page_mapping[c0x]
            elif "_" in self.error_page_mapping:
                func = self.error_page_mapping["_"]

        if not func:
            func = self._default_error_page
        _logger.debug(f"error page function:: {func}")

        co = code
        msg = message
        exp = explain

        args_def = get_function_args(func, None)
        kwargs_def = get_function_kwargs(func, None)

        args = []
        for n, t in args_def:
            _logger.debug(f"set value to error_page function -> {n}")
            if co is not None:
                if t is None or t == int:
                    args.append(co)
                    co = None
                    continue
            if msg is not None:
                if t is None or t == str:
                    args.append(msg)
                    msg = None
                    continue
            if exp is not None:
                if t is None or t == str:
                    args.append(exp)
                    exp = None
                    continue
            args.append(None)

        kwargs = {}
        for n, v, t in kwargs_def:
            if co is not None:
                if (t is None and isinstance(v, int)) or t == int:
                    kwargs[n] = co
                    co = None
                    continue
            if msg is not None:
                if (t is None and isinstance(v, str)) or t == str:
                    kwargs[n] = msg
                    msg = None
                    continue
            if exp is not None:
                if (t is None and isinstance(v, str)) or t == str:
                    kwargs[n] = exp
                    exp = None
                    continue
            kwargs[n] = v

        if args and kwargs:
            return func(*args, **kwargs)
        elif args:
            return func(*args)
        elif kwargs:
            return func(**kwargs)
        else:
            return func()

class HTTPServer(TCPServer, RoutingConf):

    allow_reuse_address = 1    # Seems to make sense in testing environment

    _default_max_workers = 50

    def server_bind(self):
        """Override server_bind to store the server name."""
        TCPServer.server_bind(self)
        host, port = self.server_address[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port

    def __init__(self, addr, res_conf={}, max_workers: int = None):
        TCPServer.__init__(self, addr, SocketServerStreamRequestHandlerWraper)
        RoutingConf.__init__(self, res_conf)
        self.max_workers = max_workers or self._default_max_workers
        self.threadpool: ThreadPoolExecutor = ThreadPoolExecutor(
            thread_name_prefix="ReqThread",
            max_workers=self.max_workers)
        self.__ready = False

    def process_request_thread(self, request, client_address):
        try:
            self.finish_request(request, client_address)
        except Exception:
            self.handle_error(request, client_address)
        finally:
            self.shutdown_request(request)

    # override
    def process_request(self, request, client_address):
        self.threadpool.submit(self.process_request_thread, request, client_address)

    @property
    def ready(self):
        return self.__ready

    def server_close(self):
        super().server_close()
        self.threadpool.shutdown(True)

    def start(self):
        try:
            self.__ready = True
            self.server.start()
        except:
            self.__ready = False
            raise

    def _shutdown(self) -> None:
        _logger.debug("shutdown http server in a seperate thread..")
        super().shutdown()

    def shutdown(self) -> None:
        threading.Thread(target=self._shutdown, daemon=False).start()

    def map_controller(self, ctrl: TaskFunction):
        url = ctrl.url
        regexp = ctrl.regexp
        method = ctrl.method
        _logger.debug(
            f"map url {url}|{regexp} with method[{method}] to function {ctrl.func}. ")
        assert method is None or method == "" or method.upper() in self.HTTP_METHODS
        _method = method.upper() if method is not None and method != "" else "_"
        if regexp:
            self.method_regexp_mapping[_method][regexp] = ctrl
        else:
            _url = remove_url_first_slash(url)

            path_pattern, path_names = get_path_reg_pattern(_url)
            if path_pattern is None:
                self.method_url_mapping[_method][_url] = ctrl
            else:
                self.path_val_url_mapping[_method][path_pattern] = (
                    ctrl, path_names)

    def _res_(self, path, res_pre, res_dir):
        fpath = os.path.join(res_dir, path.replace(res_pre, ""))
        _logger.debug(f"static file. {path} :: {fpath}")
        fext = os.path.splitext(fpath)[1]
        ext = fext.lower()
        if ext in (".html", ".htm", ".xhtml"):
            content_type = "text/html"
        elif ext == ".xml":
            content_type = "text/xml"
        elif ext == ".css":
            content_type = "text/css"
        elif ext in (".jpg", ".jpeg"):
            content_type = "image/jpeg"
        elif ext == ".png":
            content_type = "image/png"
        elif ext == ".webp":
            content_type = "image/webp"
        elif ext == ".js":
            content_type = "text/javascript"
        elif ext == ".pdf":
            content_type = "application/pdf"
        elif ext == ".mp4":
            content_type = "video/mp4"
        elif ext == ".mp3":
            content_type = "audio/mp3"
        else:
            content_type = "application/octet-stream"

        return StaticFile(fpath, content_type)