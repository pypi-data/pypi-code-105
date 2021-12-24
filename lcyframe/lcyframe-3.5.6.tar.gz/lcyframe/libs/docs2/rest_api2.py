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
            self.content += "### " + _leve_str + "、 " + resource_text[0]["model"] + "\n"

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
            self.content += "\n```python"
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

    def set_response(self, data, type=''):
        if type:
            type += "."
        for key, value in data.items():
            if value.get('rename'):
                key = value['rename']
            description = ""
            if value.get('description', ""):
                description = value['description'].replace('|', '、')
            self.content += "|" + type + key + "|" + value['type'] + "|" + description + "|\n"
            if (value['type'] in ["dict", "object_ref"]) and value.get('schema'):
                self.set_response(value['schema'], "{" + key + "}")
            if (value['type'] == "list") and value.get('items'):
                if value['items'].get('$ref'):
                    ref = value['items']['$ref']
                    schema = ref.split('/')[-1]
                    responses_data = self.definitions[schema]
                    self.set_response(responses_data['properties'], "[" + key + "].{i}")
                else:
                    self.set_response(value['items'], "[" + key + "].{i}")

    def make_req_demo(self, parameters, method, uri):
        """

        :return:
        """
        demo = self.make_req_data(parameters, {})
        if '{' in uri:
            path_params = {}
            for k in demo.keys():
                if k in uri:
                    path_params[k] = demo.pop(k, None)
            url = uri.format(**path_params)
        else:
            url = uri
        con = ""
        if method.upper() == "GET":
            con += urllib.urlencode(demo)
        if method.upper() == "POST":
            con += utils.to_json(demo)
        con += "\n"
        return con

    def make_req_data(self, rule, data):
        """

        :param rules:
        :return:
        """
        if isinstance(rule, dict):
            if rule.get('type') == "dict" and isinstance(rule.get('schema'), list):
                self.make_req_data(rule.get('schema'), data)
            else:
                data = self.filling_params(**rule)
            return data
        if isinstance(rule, list):
            for _rule in rule:
                data[_rule.get('name')] = self.make_req_data(_rule, {})
            return data

    def filling_params(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        param_name = kwargs.get('name', None)
        example = kwargs.get('example', None)
        if example:
            return example
        default = kwargs.get('default', None)
        if default:
            return default
        allow = kwargs.get('allow', None)
        if allow:
            return random.choice(allow)
        params_type = kwargs.get('type')
        if params_type in ['int', 'integer', 'number', 'long']:
            if param_name:
                if 'date' in param_name:
                    return 20170803
            return random.randint(1, 100)
        elif params_type in ['str', 'string', 'str', 'unicode', 'bytes']:
            if param_name:
                if 'mobile' in param_name:
                    return "18888888888"
                elif 'phone' in param_name:
                    return "18888888888"
                elif 'tel' in param_name:
                    return "010-88886666"
                elif 'address' in param_name:
                    return "xxx市xxx省xxx"
                elif 'id' in param_name:
                    return random.choice(["5826650e3d65ce2d0665317f",
                                          "582661953d65ce2b7b5dde32",
                                          "5826650e3d65ce2d27645763",
                                          "580cb92e3d65ce09ebf7dc4e"])
                elif 'shipping_time' in param_name:
                    return "11:45"
                elif 'name' in param_name:
                    return random.choice(["驴与鱼", "绿与鱼", '绿与驴', '驴与绿', '小犟驴'])
                elif 'code' in param_name:
                    return ''.join(random.sample(string.digits, 6))
            return ''.join(random.sample(string.ascii_letters + string.digits, 6))
        elif params_type in ['bool', 'boolean']:
            return bool(random.getrandbits(1))
        elif params_type in ['date']:
            return int(datetimeutil.prc_now("%Y%m%d"))
        elif params_type in ['datetime']:
            return "2017-09-15T03:49:58.060000+00:00"
        elif params_type in ['float']:
            return random.uniform(30, 120)
        elif params_type in ['dict']:
            return {}
        elif params_type in ['list']:
            if param_name:
                if 'poi' in param_name:
                    return [116.23233, 39.12322]
            return []
        elif params_type in ['ObjectId', "objectid"]:
            return random.choice(["5826650e3d65ce2d0665317f",
                                  "582661953d65ce2b7b5dde32",
                                  "5826650e3d65ce2d27645763",
                                  "580cb92e3d65ce09ebf7dc4e"])
        return None

    def make_resp_demo(self, responses, uri):
        """

        :param responses:
        :param uri:
        :return:
        """
        if responses.get("200"):
            ref = responses['200']['schema']['$ref']
        else:
            ref = responses['201']['schema']['$ref']
        schema = ref.split('/')[-1]
        responses_data = self.definitions[schema]
        properties = responses_data.get('properties')
        if properties.get('_meta'):
            # object-set
            set_item_schema_ref = properties['results']['items']['$ref']
            result_ref = set_item_schema_ref.lstrip('#/definitions/')
            result = self.definitions.get(result_ref, None)
            if not result:
                print("[Error]:", result_ref, ' URL:', uri, ", not defind response schema.")
                exit()
            else:
                result = self.make_resp_date(result.get('properties'), {})
                _result = {
                    "_meta": {
                        "has_more": True,
                        "result_count": random.randint(1, 10),
                    },
                    "data": [result]
                }
                return utils.to_json(_result)
        else:
            _result = self.make_resp_date(properties, {})
            return utils.to_json(_result)

    def make_resp_date(self, properties, data):
        if not isinstance(properties, dict):
            print("[Error]: response schema defind error.")
            exit()
        for param_name, rule in properties.items():
            if rule.get('rename'):
                param_name = rule.get('rename')
            if rule.get('type') and rule.get('type') in ["object_ref", 'dict'] and rule.get('schema'):
                data[param_name] = self.make_resp_date(rule.get('schema'), {})
            else:
                data[param_name] = self.filling_params(name=param_name, **rule)
        return data

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