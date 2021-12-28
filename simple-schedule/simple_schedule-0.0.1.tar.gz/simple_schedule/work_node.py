import os
import threading
import inspect
import importlib
import re

from simple_schedule.logger import get_logger,set_level
from typing import Dict
from simple_schedule import http_server
from simple_schedule import  _get_request_mappings,  _get_error_pages

__logger = get_logger("simple_schedule.work_node")

__SENSE_MODULE = ""
__HTTP_RESOURCE: Dict[str, str] = {}  #http static resource

def _is_match(string="", regx=r""):
    if not regx:
        return True
    pattern = re.compile(regx)
    match = pattern.match(string)
    return True if match else False


def _to_module_name(fpath="", regx=r""):
    fname, fext = os.path.splitext(fpath)

    if fext != ".py":
        return
    mname = fname.replace(os.path.sep, '.')
    if _is_match(fpath, regx) or _is_match(fname, regx) or _is_match(mname, regx):
        return mname


def _load_all_modules(work_dir, pkg, regx):
    abs_folder = work_dir + "/" + pkg
    all_files = os.listdir(abs_folder)
    modules = []
    folders = []
    for f in all_files:
        if os.path.isfile(os.path.join(abs_folder, f)):
            mname = _to_module_name(os.path.join(pkg, f), regx)
            if mname:
                modules.append(mname)
        elif f != "__pycache__":
            folders.append(os.path.join(pkg, f))

    for folder in folders:
        modules += _load_all_modules(work_dir, folder, regx)
    return modules


def _import_module(mname):
    try:
        importlib.import_module(mname)
    except:
        __logger.warning(f"Import moudle [{mname}] error!")


def scan(base_dir: str = "", regx: str = r"", project_dir: str = "") -> None:
    if project_dir:
        work_dir = project_dir
    else:
        ft = inspect.currentframe()
        fts = inspect.getouterframes(ft)
        entrance = fts[-1]
        work_dir = os.path.dirname(inspect.getabsfile(entrance[0]))
    modules = _load_all_modules(work_dir, base_dir, regx)

    for mname in modules:
        __logger.info(f"Import controllers from module: {mname}")
        _import_module(mname)

__lock = threading.Lock()
_server = None

def start(appName = "" ,host="", port: int = 8132,max_workers: int = None):
    """start work node """
    with __lock:
        global _server
        if _server is not None:
            _server.shutdown()
        __logger.info(f"Start app {appName} in threading mixed mode, listen to port {port}")
        _server = http_server.HTTPServer(host,port,__HTTP_RESOURCE,max_workers = max_workers)
    
    
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    _server.scan(project_dir=root, base_dir="./sense",
                    regx=r'.*')

    request_mappings = _get_request_mappings()
    # request mapping
    for ctr in request_mappings:
        _server.map_controller(ctr)
    
    err_pages = _get_error_pages()
    for code, func in err_pages.items():
        _server.map_error_page(code, func)

    # start the server
    _server.start()

        
                                                          
        
