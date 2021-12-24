# -*- coding:utf-8 -*-
import sys
from importlib import import_module
import os, glob, re
from datetime import datetime
from bson import ObjectId
from pathlib import Path

class AnanasDBTable(object):

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
        self.kwargs = kwargs

    def set_md(self):
        """

        :return:
        """
        self.make_mk_str()
        self.write_file()

    def make_mk_str(self, schema_dir=None):
        """

        :return:
        """

        if not self.if_set:
            return

        file = schema_dir or os.path.join(self.module_dir, self.module_name)

        try:
            for schema_dir in glob.glob("%s/*" % file):
                schema_dir = Path(schema_dir).as_uri()
                if "__pycache__" in schema_dir:
                    continue

                objs_mp = {}
                content = ""

                if os.path.isdir(schema_dir):
                    self.make_mk_str(schema_dir)
                else:
                    model_name = schema_dir.replace(self.ROOT, "").lstrip("/").replace("/", ".").replace(".py", "")
                    objs = import_module(model_name)

                    for p in dir(objs):
                        if p.startswith("__"):
                            continue

                        if p == "BaseSchema":
                            continue

                        if type(getattr(objs, p)) != type:
                            continue

                        if not hasattr(getattr(objs, p), "collection"):
                            continue

                        if not getattr(getattr(objs, p), "collection"):
                            continue

                        # 字段：getattr(objs, "DemoSchema")()
                        # 类属性：getattr(objs, "DemoSchema")
                        objs_mp[p] = getattr(objs, p)

                    __, filename = os.path.split(schema_dir)
                    if not re.findall('[A-Za-z]\w+_schema\.py$', filename):
                        continue
                    try:
                        with open(schema_dir, "r", encoding="utf-8") as p:
                            find_class = False
                            schema_obj = None
                            fields = []
                            for line in p.readlines():
                                # 源码模式显示
                                # if find_class is False:
                                #     if re.findall(r'class\s+(.+?)Schema[(]BaseSchema[)]:', line):
                                #         find_class = True
                                #         content += line
                                # else:
                                #     if "@classmethod" in line or "@staticmethod" in line:
                                #         break
                                #     elif "__init__(self)" not in line and re.findall(r'def\s+(.+?)[(].*?[)]:', line):
                                #         break
                                #     else:
                                #         # if "def __init__(self):" in line:
                                #         #     content += line.replace("def __init__(self):", "数据库字段如下：")
                                #         # else:
                                #         #     content += line.replace("self.", "")
                                #         content += line.replace("self.", "")

                                result = re.findall(r'class\s+(.+?)[(]BaseSchema[)]:', line)
                                if find_class is False:
                                    if result:
                                        find_class = True
                                        schema_name = result[0]
                                        schema_obj = objs_mp[schema_name]
                                        content = self.get_table_name(schema_obj, content)
                                # 发现另外一个Schema，先把当前收集到的字段组装完成
                                elif result:
                                    content = self.get_field_data(schema_obj, fields, content)

                                    # 另一个表
                                    schema_name = result[0]
                                    schema_obj = objs_mp[schema_name]
                                    content = self.get_table_name(schema_obj, content)
                                    fields = []
                                    fields = self.get_fields(fields, line)
                                else:
                                    if "@classmethod" in line or "@staticmethod" in line:
                                        continue
                                    elif "__init__(self)" not in line and re.findall(r'def\s+(.+?)[(].*?[)]:', line):
                                        continue
                                    elif "self." not in line:
                                        continue
                                    else:
                                        fields = self.get_fields(fields, line)

                            content = self.get_field_data(schema_obj, fields, content)

                            self.docs += content
                    except Exception as e:
                        self.docs += "生成失败 %s:%s\n" % (schema_name, str(e))
        except Exception as e:
            self.docs += "生成失败：%s, %s\n" % (file, str(e))

        self.docs = self.title + self.docs

    def get_table_name(self, schema_obj, content):
        """
        获取表名
        :param result:
        :param objs_mp:
        :param content:
        :return:
        """
        collection = schema_obj.collection
        content += "###" + "表: " + collection + "\n"
        content += "说明:" + schema_obj.__doc__.lstrip("\n").rstrip(" ")
        return content

    def get_fields(self, fields, line):
        """
        获取字段
        :param fields:
        :param line:
        :return:
        """
        try:
            line = line.replace("\n", "")
            # 字段定义与描述
            result = re.findall(r'\s+self.(.+?)\s+=\s+(.*?)\s*(#.*?)$', line) or \
                     re.findall(r'\s+self.(.+?)\s+=\s+(.*?)\s*(#.*?)$', line) or \
                     re.findall(r'\s+self.(.+?)\s+=\s+(.*?)$', line)
            if result:
                fields.append(result[0])
        except Exception as e:
            pass
        finally:
            return fields

    def get_field_data(self, obj, fields, content):
        """
        组装指定表的字段结构
        :param class_name:
        :param fields:
        :return:
        """
        def _get_max_len():
            max_len = 0
            for item in fields:
                field_id = item[0]
                v = getattr(obj(), field_id)
                if ObjectId.is_valid(v):
                    v = len(str(v))
                elif isinstance(v, datetime):
                    v = 20
                elif isinstance(v, (dict, list, tuple)):
                    v = 10
                else:
                    v = len(str(v))

                if v > max_len:
                    max_len = v

            return max_len

        max_len = _get_max_len()

        content += "~~~python\n"
        for item in fields:
            if len(item) > 2:
                field_id = item[0]
                default_default = item[1]
                desc = item[2]
            else:
                field_id = item[0]
                default_default = item[1]
                desc = ""

            v = getattr(obj(), field_id)
            if ObjectId.is_valid(v):
                v = str(v)
            elif isinstance(v, datetime):
                v = "datatime日期格式"
            elif isinstance(v, dict):
                pass

            # 对于数字，当他是字符类型时，加双引号
            if type(v) in [int, float, bool]:
                content += '%s = %s' % (field_id, v)
                space_len = max_len - (len(str(v)) + len(field_id)) + 2
            elif type(v) in [tuple, list, dict]:
                content += '%s = %s' % (field_id, self.set_resp_md(v))
                if not v:
                    space_len = max_len - (0 + len(field_id))
                else:
                    space_len = max_len - 1 + 5
            else:
                content += '%s = "%s"' % (field_id, v)
                space_len = max_len - (len(str(v)) + len(field_id))

            content += ' ' * (space_len+10) + desc + "\n"

        content += "~~~\n"

        return content

    def set_resp_md(self, str_data):
        """

        :return:
        """
        str_v = ""
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
                        "bool": float,
                        "dict": dict,
                        "json": ""}
            # suffix = ""
            # for t, v in STR2TYPE.items():
            #     if "|%s" % t in str(obj):
            #         obj = obj.replace("|%s" % t, "")
            #         suffix = ", 类型%s" % t
            #
            # s = ""
            # s += str(obj) + suffix
            # return s + ",\n"

            if type(obj) in [str]:
                s = '"%s"' % obj
            elif type(obj) == bytes:
                s = '"%s"' % obj.decode("u8")
            else:
                s = str(obj)
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
            str += "[\n"
            for item in obj:
                # str += "\n"
                str += space + "   " + get_type_fun(item)
                # str += space + "   ...,\n"
                # break

            str += space + "],"
            str += "\n"
            self.space_seq -= 1
            return str

        if type(str_data) == dict:
            for key, value in str_data.items():
                str_v += get_space()
                str_v += "\"%s\"" % key + ": " + get_type_fun(value)
                self.space_seq = 1
        else:
            for value in str_data:
                str_v += get_space()
                str_v += get_type_fun(value)
                self.space_seq = 1

        if type(str_data) == dict:
            return "{\n" + str_v + "}" if str_data else "{" + str_v + "}"
        else:
            return "[\n" + str_v + "]" if str_data else "[" + str_v + "]"

    def write_file(self):
        file_dir = self.path + "/docs/tables.md"
        f = open(file_dir, "w+", encoding='utf-8')
        f.write(self.docs)
        f.close()

