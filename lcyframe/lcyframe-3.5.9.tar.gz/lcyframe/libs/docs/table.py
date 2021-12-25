# -*- coding:utf-8 -*-
import sys, datetime
from lcyframe.libs import yaml2py

class AnanasTable(object):

    def __init__(self, **kwargs):
        self.path = kwargs.get('path')
        self.index_doc_config = kwargs.get('index_doc_config')

    def set_index(self):
        """

        :return:
        """
        title = self.index_doc_config.get('title')
        navs = self.index_doc_config.get('nav')
        content = ".. LcyFrame documentation\n\n"
        content += title + "\n" + len(title) * 2 * "=" + "\n\n"
        content += self.index_doc_config.get('content') + "\n\n"
        content += "目录: \n\n"
        content += ".. toctree::\n   :maxdepth: 2\n\n"

        if not navs:
            content += "   docs/" + "api" + ".md\n"
        else:
            for nav in navs:
                content += "   docs/" + nav + ".md\n"

        content += "\n\n"
        f = open(self.path + '/index.rst', "w+", encoding='utf-8')
        f.write(content)
        f.close()


