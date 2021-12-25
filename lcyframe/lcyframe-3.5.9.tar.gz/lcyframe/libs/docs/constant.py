# -*- coding:utf-8 -*-
import sys
from importlib import import_module
from pathlib import Path


class AnanasConstant(object):

    docs = ""
    constant_docs = ""

    def __init__(self, **kwargs):
        """

        :param if_set:
        :param module_dir:
        :param module_name:
        :param title:
        """
        self.ROOT = kwargs["ROOT"]
        self.if_set = kwargs.get('if_set')
        self.module_dir = kwargs.get('module_dir')
        self.module_name = kwargs.get('module_name')
        self.title = kwargs["title"]
        self.title = "\n\n## " + self.title + "\n\n"
        self.path = kwargs.get('path')

    def set_md(self):
        """

        :return:
        """
        self.make_mk_str()
        self.write_file()

    def make_mk_str(self):
        """

        :return:
        """

        if not self.if_set:
            return

        # model_name = self.module_dir.replace(self.ROOT, "").lstrip("/").replace("/", ".") + "." + self.module_name.rstrip(".py")
        file = self.module_dir + "/" + self.module_name + ".py"
        try:
            with open(file, "r", encoding="utf-8") as p:
                content = p.read()
        except Exception as e:
            content = "生成失败：%s" % file.replace(self.ROOT, "")

        self.docs += "~~~python\n"
        self.docs += content + "\n"
        self.docs += "~~~\n"

        self.docs = self.title + self.docs

    def write_file(self):
        file_dir = self.path + "/docs/constant.md"
        f = open(file_dir, "w+", encoding='utf-8')
        f.write(self.docs)
        f.close()

