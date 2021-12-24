# -*- coding:utf-8 -*-
import os
import sys
import logging
from . import error
from . import log
from . import table
from . import rest_api
from . import constant
from . import db_table
import platform

from importlib import import_module


class AnanasTemplate(object):

    def __init__(self, app, path):
        self.app = app
        self.path = path

    def run(self, executable):
        """

        :return:
        """
        config = import_module(self.path.replace(self.app.ROOT, "").lstrip("/").replace("/", ".") + ".conf")
        errors_doc_config = config.errors_doc_config
        log_doc_config = config.log_doc_config
        index_doc_config = config.index_doc_config
        api_doc_config = config.api_doc_config
        constant_doc_config = config.constant_doc_config
        table_doc_config = config.table_doc_config

        # make version
        if log_doc_config.get('if_set_log') is True:
            os.system("vim " + path + "/template/_version/.note")
            os.system("vim " + path + "/template/_version/.version")

        # make markdown
        self.make_markdown(errors_doc_config=errors_doc_config,
                           log_doc_config=log_doc_config,
                           index_doc_config=index_doc_config,
                           api_doc_config=api_doc_config,
                           constant_doc_config=constant_doc_config,
                           table_doc_config=table_doc_config)
        # remove cache
        try:
            os.remove("rm -rf " + self.path + "/build")
        except:
            pass

        # make html
        if self.app.api_docs.get("stdout", False) is False:
            if platform.system() == "Windows":
                stdout = "> NUL"
            else:
                stdout = "> /dev/null 2>&1"
        else:
            stdout = ""
        os.system("%s -msphinx -M html " % executable + self.path + " " + self.path + "/build %s" % stdout)
        logging.warning('Docs Running on http://%s:%s/docs' % (self.app.uri, self.app.port))

    def make_markdown(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        # load config
        errors_doc_config = kwargs.get('errors_doc_config')
        log_doc_config = kwargs.get('log_doc_config')
        index_doc_config = kwargs.get('index_doc_config')
        api_doc_config = kwargs.get('api_doc_config')
        constant_doc_config = kwargs.get('constant_doc_config')
        table_doc_config = kwargs.get('table_doc_config')

        # make api md
        if api_doc_config.get("if_set_api") is True:
            api_server = rest_api.AnanasRestApi(path=self.path, api_doc_config=api_doc_config)
            api_server.set_api()
            # print("Api document was generated successfully！")

        # make error md
        if errors_doc_config.get('if_set_errors') is True:
            error_server = error.AnanasError(ROOT=self.app.ROOT, path=self.path, **errors_doc_config)
            error_server.set_md()
            # print("Error document was generated successfully！")

        # make constant md
        if constant_doc_config.get('if_set') is True:
            constant_server = constant.AnanasConstant(ROOT=self.app.ROOT, path=self.path, **constant_doc_config)
            constant_server.set_md()

        # make table md
        if table_doc_config.get('if_set') is True:
            table_server = db_table.AnanasDBTable(ROOT=self.app.ROOT, path=self.path, **table_doc_config)
            table_server.set_md()

        # make log md
        if log_doc_config.get('if_set_log') is True:
            log_server = log.AnanasLog(path=self.path,
                                       log_doc_config=log_doc_config)
            log_server.set_md()
            # print("Log document was generated successfully！")

        # make index
        table_server = table.AnanasTable(path=self.path,
                                         index_doc_config=index_doc_config)
        table_server.set_index()
        # print("Index document was generated successfully！")

        # init log
        if log_doc_config.get('if_set_log') is True:
            log_server.initialize()

if __name__ == "__main__":
    path = sys.argv[1]
    AnanasTemplate(path).run(sys.executable)
