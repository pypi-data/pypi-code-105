from ctypes import c_char_p
import sys
from protectonce_native.runtimes.python.protect_once_py_interface import (
    ProtectOnceInterface,
)
import json
from .dependency import CustomEncoder, Dependency
import pkg_resources


po_interface = ProtectOnceInterface()
po_interface.init_core()


def login():
    runtime_version = "{0}.{1}.{2}".format(
        str(sys.version_info.major),
        str(sys.version_info.minor),
        str(sys.version_info.micro),
    )

    packages = []
        
    for package in pkg_resources.working_set:   
        packages.append(Dependency(package.project_name, package.version, package.platform,'static'))

    login_data = {
        "runtime": "python",
        "runtimeVersion": runtime_version,
        "bom": packages,
    }
    str_login_data = json.dumps(login_data, cls=CustomEncoder)
    result, out_data_type, out_data_size, mem_buffer_id = po_interface.invoke(
        "init", str_login_data, len(str_login_data)
    )
    result = c_char_p(result).value
    rules_data = json.loads(result.decode("utf-8"))

    released = po_interface.release(mem_buffer_id)

    return rules_data


def stop():
    po_interface.shutdown_core()
