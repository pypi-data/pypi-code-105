# -*- coding:utf-8 -*-
import os
import sys
import glob
import copy
import random
import string
import urllib
import json
from collections import OrderedDict
import logging
from . import utils
from . import datetimeutil
from . import exception as errors
from lcyframe.libs import yaml2py
from lcyframe.libs.utils import fix_path

class AnanasRestApi(object):

    content = ""

    def __init__(self, **kwargs):
        """
        加载配置文件
        """
        self.config = kwargs.get('api_doc_config')
        self.path = kwargs.get('path')
        self.schema_template = self.config.get("schema_template") or "default"
        self.api_schema_mp = {
            "lcyframe": self.process_resource_context,
        }
    def set_api(self):
        """

        :return:
        """
        self.content += "## " + self.config.get('title') + "\n\n"
        self.set_yml_md()
        self.make_md()

    def set_yml_md(self):
        """

        :return:
        """
        path = self.config.get('api_schema_dir')
        leve_str = str(self.config.get('leve')) + "."
        leve = 1

        if self.schema_template != "lcyframe":
            self.definitions = yaml2py.load_yaml_file(os.path.join(path, "definitions.yml"))
        else:
            self.definitions = {}

        try:
            if not os.path.exists(path):
                raise Exception("The docs dir not exists %s" % path)

            l = glob.glob('%s/*' % path)
            for pkg_dir in l[::-1]:
                if os.path.basename(pkg_dir) == "definitions.yml":
                    continue

                leve, leve_str = self.generate_content(pkg_dir, leve, leve_str)
        except errors.AnanasDocError as e:
            print("[Error]:" + str(e.code) + ":" + e.message)
            exit()

    def generate_content(self, path, leve, leve_str):
        """
        :param path:
        :return:
        """
        if os.path.isdir(path):
            for p in os.listdir(path):
                return self.generate_content(fix_path(os.path.join(path, p)), leve, leve_str)
        else:
            if path.split(".")[-1] != "yml":
                logging.warning("the %s is not .yml format." % path)
                raise Exception("the %s is not .yml format." % path)

            resource_text = yaml2py.load_yaml_file(path, False)
            _leve_str = leve_str + str(leve)

            if not resource_text:
                return

            if "model" not in resource_text[0]:
                logging.warning("require key 'model' in %s " % path)

            model_name = resource_text[0]["model"] or "未命名的模块"
            self.content += "### " + _leve_str + "、 " + model_name + "\n"

            n = 1
            for resource_def in resource_text:
                # _leve_str = leve_str + str(leve)
                self.api_schema_mp[self.schema_template](resource_def, _leve_str, n)
                n += 1

            leve += 1

        return leve, leve_str

    def process_resource_context(self, resource_def, _leve_str, n):
        """

        :param resource_def:
        :param leve_str:
        :return:
        """
        uri = resource_def["apis"]
        for method, data_mp in resource_def['method'].items():
            self.content += "#### " + _leve_str + "." + str(n) + "、"
            self.content += (data_mp.get('summary', {}) or "功能名称") + "\n"
            if data_mp.get('description', ""):
                self.content += "**说明：%s**\n\n" % str(data_mp.get('description', "") or "方法说明")
            self.content += "**接口：**<strong><font color='#e48928' size='4px'>%s</font></strong>\n\n" % uri
            if method.upper() == "GET":
                color_value = "#2eae21"
            elif method.upper() == "POST":
                color_value = "#ec899a"
            elif method.upper() == "PUT":
                color_value = "#3de485"
            else:
                color_value = "#eb1c44"
            self.content += "**方法：**<font color='%s'><b>%s</b></font>\n\n" % (color_value, method.upper())
            self.content += "**参数：**\n\n"
            self.content += "|参数|类型|必须|允许值|描述|\n"
            self.content += "|:--------|:--------|:------|:--------|:------|\n"

            # request params
            parameters = data_mp.get('parameters', [])
            if not parameters:
                self.content += "|_|_|_|_|_|\n"
            self.set_req_md(copy.deepcopy(parameters))

            # response params
            self.content += "\n**成功响应：**\n"
            self.content += "\n```python"
            self.content += "\n"

            responses = data_mp.get('responses', None)
            if responses:
                self.set_resp_md(copy.deepcopy(responses))
            else:
                self.content += "{\n\n}\n"

            self.content += "\n```\n"

            # reference
            # reference = data_mp.get("reference", "")
            # self.set_reference_md(reference)

    def generate_content2(self, path, leve, leve_str):
        """
        风格2：文档作出导航，按照以下三级节点生成
        模块：
            handler
                get
                post
                delete
                put
        :param path:
        :param leve:
        :param leve_str:
        :return:
        """
        if os.path.isdir(path):
            for p in os.listdir(path):
                return self.generate_content(fix_path(os.path.join(path, p)), leve, leve_str)
        else:
            if path.split(".")[-1] != "yml":
                logging.warning("the %s is not .yml format." % path)
                raise Exception("the %s is not .yml format." % path)

            resource_text = yaml2py.load_yaml_file(path, False)
            _leve_str = leve_str + str(leve)

            if not resource_text:
                return

            if "model" not in resource_text[0]:
                logging.warning("require key 'model' in %s " % path)
            self.content += "### " + _leve_str + "、 " + resource_text[0]["model"] + "\n"

            n = 1
            for resource_def in resource_text:
                # _leve_str = leve_str + str(leve)
                self.api_schema_mp[self.schema_template](resource_def, _leve_str, n)
                n += 1

            leve += 1

        return leve, leve_str

    def process_resource_context2(self, resource_def, _leve_str, n):
        """

        :param resource_def:
        :param leve_str:
        :return:
        """
        uri = resource_def["apis"]
        name = resource_def.get('name', "") or "未命名的模块"
        self.content += "#### " + _leve_str + "." + str(n) + "、" + name + "\n"

        description = resource_def.get('description')
        if description:
            self.content += "**说明：**" + description + "\n"

        leve = 1
        for method, data_mp in resource_def['method'].items():
            self.content += "##### " + _leve_str + "." + str(n) + "." + str(leve) + "、"
            self.content += (data_mp.get('summary', {}) or "功能名称") + "\n"
            if data_mp.get('description', ""):
                self.content += "**说明：%s**\n\n" % str(data_mp.get('description', "") or "方法说明")
            self.content += "**接口：**<strong><font color='#e48928' size='4px'>%s</font></strong>\n\n" % uri
            if method.upper() == "GET":
                color_value = "#2eae21"
            elif method.upper() == "POST":
                color_value = "#ec899a"
            elif method.upper() == "PUT":
                color_value = "#3de485"
            else:
                color_value = "#eb1c44"
            self.content += "**方法：**<font color='%s'><b>%s</b></font>\n\n" % (color_value, method.upper())
            self.content += "**参数：**\n\n"
            self.content += "|参数|类型|必须|允许值|描述|\n"
            self.content += "|:--------|:--------|:------|:--------|:------|\n"

            # request params
            parameters = data_mp.get('parameters', [])
            if not parameters:
                self.content += "|_|_|_|_|_|_|\n"
            self.set_req_md(copy.deepcopy(parameters))

            # response params
            self.content += "\n**成功响应：**\n"
            self.content += "\n```json"
            self.content += "\n"

            responses = data_mp.get('responses', None)
            if responses:
                self.set_resp_md(copy.deepcopy(responses))
            else:
                self.content += "{\n\n}\n"

            self.content += "\n```\n"

            leve += 1

    def set_req_md(self, rules):
        """

        :return:
        """
        if type(rules) == list:
            for rule in rules:
                self.set_req_params_md(rule)
                if rule['type'] == 'dict':
                    if rule.get('schema'):
                        self.set_req_md(rule)
        if type(rules) == dict:
            if rules['type'] == 'dict':
                for rule in rules['schema']:
                    rule['name'] = "{" + rules['name'] + "}." + rule.get('name', '')
                    self.set_req_params_md(rule)

    def set_req_params_md(self, rule):
        """

        :param content:
        :return:
        """
        required = rule.get('required', None)
        if required is True:
            rule['required'] = "是"
        else:
            rule['required'] = "否"

        if not rule.get('description'):
            rule["description"] = "无说明"

        description = str(rule['description']).replace('|', '、')

        en_value_str = ""
        if rule.get('allow', []):
            en_value_str = ", ".join(map(str, rule["allow"]))
        if rule.get('allowed', []):
            en_value_str = ", ".join(map(str, rule["allowed"]))

        self.content += "|" + '<font color="#9d127b"><strong>' + rule['name'] + '</strong></font>' + \
                        "|" + rule['type'] + \
                        "|" + rule['required'] + \
                        "|" + en_value_str + \
                        "|" + str(description) + \
                        "|\n"       # "|" + rule.get("in", "query") + \

    def set_resp_md(self, responses):
        """
        响应数据组装
        :return:
        """
        self.space_seq = 1

        def get_space():
            return self.space_seq * "   "

        def get_type_fun(obj):
            t = type(obj)
            if t in [dict, list, tuple]:
                return {
                    dict: gen_dict_obj,
                    list: gen_list_obj,
                    tuple: gen_list_obj,
                }[t](obj)
            else:
                return get_string_obj(obj)

        def get_string_obj(obj):
            STR2TYPE = {"int": int,
                        "integer": int,
                        "string": str,
                        "str": str,
                        "unicode": "",
                        "float": float,
                        "bool": bool,
                        "dict": dict,
                        "json": ""}
            suffix = ""
            for t, v in STR2TYPE.items():
                if "|%s" % t in str(obj):
                    # 代码模式下，冲突的字符导致样式失效，需要替换
                    if type(obj) in [str, bytes] and "|" in obj:
                        if "，" in obj:
                            obj = obj.replace("，", ",")
                        if "：" in obj:
                            obj = obj.replace("：", ":")
                        if '"' in obj:
                            obj = obj.replace('"', "'")
                        if '（' in obj:
                            obj = obj.replace('（', "(")
                        if '）' in obj:
                            obj = obj.replace('）', ")")
                        if '；' in obj:
                            obj = obj.replace('；', ";")

                    obj = obj.replace("|%s" % t, "")
                    suffix = ", 类型%s" % t

            # if type(obj) in [str, unicode]:
            #     obj = "\"" + obj + "\""
            #
            #     obj = obj + suffix

            # 1、字符串类型的数字、文字，需要加双引号
            # 2、整形，浮点型，bool类型的值不需要
            s = ""
            if type(obj) in [str, bytes] and "类型" not in suffix:
                s += '"%s"' % (str(obj) + suffix)
            else:
                s += str(obj) + suffix
            return s + ",\n"

        def gen_dict_obj(obj):
            self.space_seq += 1
            space = get_space()

            str = ""
            # str += "\n"
            str += "{\n"
            for k, n in obj.items():
                str += space + "  \"%s\"" % k + ": " + get_type_fun(n)
            str += space + "},\n"
            self.space_seq -= 1
            return str

        def gen_list_obj(obj):
            self.space_seq += 1
            space = get_space()

            str = ""
            # str += "\n"
            str += "["
            for item in obj:
                str += "\n"
                str += space + "   " + get_type_fun(item)
                str += space + "   ...,\n"
                break

            str += space + "],"
            str += "\n"
            self.space_seq -= 1
            return str

        self.content += "{\n"

        for key, value in responses.items():
            self.content += get_space()
            self.content += "\"%s\"" % key + ": " + get_type_fun(value)
            self.space_seq = 1

        self.content += "}" if responses else "\n}"

    def set_reference_md(self, reference):
        """
        组装参考描述
        :param reference:
        :return:
        """
        if not reference:
            return

        self.content += "**参考说明：**\n"
        self.content += "```dart\n"
        for index, s in enumerate(reference.split("\\")):
            self.content += str(index+1)
            self.content += s + "\n"

        self.content += "```\n"

    def make_md(self):
        """

        :return:
        """

        f = open(self.path + '/docs/api.md', "w+", encoding='utf-8')
        f.write(self.content)
        f.close()




if __name__ == "__main__":
    kw = {
        "api_doc_config": {
            "if_set_api": True,
            "api_schema_dir": "/Users/Song/Desktop/www/docs/api_schema",
            "leve": 2,
            "title": "接口文档",
            "schema_template": "lcylln"
        },
        'path': "/Users/Song/Desktop/www/docs/doc",

    }
    a = AnanasRestApi(**kw)
    a.set_api()