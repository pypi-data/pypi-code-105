# -*- coding: utf-8 -*-
"""
docs

"""
import os, io
from os import path
import sys
import shutil
from . import conf
from . import makefile
from lcyframe.libs import pytemplate
from lcyframe.libs import Copyright

package_dir = path.abspath(path.dirname(__file__))

try:
    # check if colorama is installed to support color on Windows
    import colorama
except ImportError:
    colorama = None

if False:
    # For type annotation
    from typing import Dict  # NOQA

codes = {}  # type: Dict[str, str]

def mkdir(path):
    """

    :param path:
    :return:
    """
    path = path.strip()
    path = path.rstrip("\\")

    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path)
    else:
        pass


def color_terminal():
    # type: () -> bool
    if sys.platform == 'win32' and colorama is not None:
        colorama.init()
        return True
    if not hasattr(sys.stdout, 'isatty'):
        return False
    if not sys.stdout.isatty():
        return False
    if 'COLORTERM' in os.environ:
        return True
    term = os.environ.get('TERM', 'dumb').lower()
    if term in ('xterm', 'linux') or 'color' in term:
        return True
    return False

def nocolor():
    # type: () -> None
    if sys.platform == 'win32' and colorama is not None:
        colorama.deinit()
    codes.clear()


def main(project_name, path, api_schema_dir, errors_dir, constant_dir, model_dir):
    if not color_terminal():
        nocolor()
    error = "MakeError:[%s]"

    # make project dir
    try:
        if not path:
            print(error % "Please enter the project name")
            exit()
    except:
        print(error % "Please enter the project name")
        exit()

    is_exists = os.path.exists(path)
    if is_exists:
        print(error % "The directory already exists, do not duplicate it")
        exit()

    docs_path = path + "/docs"
    mkdir(path)
    mkdir(docs_path)

    with open(docs_path + "/api.md", "w", encoding='utf-8') as p:
        p.write("")

    with open(docs_path + "/agree.md", "w", encoding='utf-8') as w:
        w.write(pytemplate.get_docs_agree())

    with open(docs_path + "/error.md", "w", encoding='utf-8') as p:
        p.write("##三、错误码说明")

    # mkconf
    conf_server = conf.Config(path=path)
    conf_server.config_dict['project'] = project_name + "接口文档"
    conf_server.config_dict['copyright'] = "Document is automatic generation for %s. %s" % (Copyright.frame_name, Copyright.auto_email)
    conf_server.config_dict['author'] = Copyright.auto_name
    conf_server.mk_conf(api_schema_dir, errors_dir, constant_dir, model_dir)

    # load init files
    now_dir = path + "/template"
    shutil.copytree(package_dir + '/template', str(now_dir))
    shutil.copyfile(package_dir + '/index.rst', path + '/index.rst')
    mkfile_server = makefile.MakeFile(path=path)
    mkfile_server.set_make_file()
    # print("%s project created successfully!" % path)



if __name__ == "__main__":
    main(sys.argv[1], "", "project_name")
