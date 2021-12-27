# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 测试打标签功能
# author : 
# create_time : 2020/7/18 16:15
# update_time : 2020/7/18 16:15
# copyright : Lavector
# ----------------------------------------------
import sys,os

from maxda.analysis.da_tag.Filed_Services import VerMappingCollect

sys.path.append(os.getcwd())
import unittest

from maxda.util.panda_tool import PandaTool

from dataset.dataset_config import *
from maxda.analysis.da_tag.tag_deal import *

tag_config_path = os.path.join(example_config_path, "config_tag_mapping.xlsx")



# class TestUnitTag(unittest.TestCase):
#     def test_tag(self):
#         tag_object = TagDealSimple()
#         config = {"mappingDictPath": tag_config_path}
#         tag_object.load_config_data(**config)
#         data = {"content": "//@好运气全给五选一:#吴宣仪[超话]#  #吴宣仪雪花秀雪御活颜菁萃系列代言人#  �@火箭少女101_吴宣仪",
#                 "channel": 'weibo'
#                 }
#         tag_object.process(data)
#
#     def test_format_tag(self):
#         format_object = ResultTagFormat(intermediate="tag_result", add_head_text="tag_format_")
#         config = {"TagDictPath": tag_config_path}
#         format_object.load_config_data(**config)
#         input_data_path = os.path.join(example_test_input_path, "result_tag.xlsx")
#         df_input = PandaTool.read(input_data_path)
#         format_object.process(df_input)


# class TestUnitRelationTag(unittest.TestCase):
#     def test_relation_tag(self):
#         tag_object = TagDealRelationSimple()
#         config = {"mappingDictPath": tag_config_path}
#         tag_object.load_config_data(**config)
#         data = {"content": "//@好运气全给五选一:#吴宣仪[超话]#  #吴宣仪雪花秀雪御活颜菁萃系列代言人#  �@火箭少女101_吴宣仪",
#                 "channel": 'weibo'
#                 }
#         tag_object.process(data)
#
#     def test_format_tag(self):
#         format_object = ResultTagFormat(intermediate="tag_rel_result", add_head_text="tag_format_")
#         config = {"TagDictPath": tag_config_path}
#         format_object.load_config_data(**config)
#         input_data_path = os.path.join(example_test_input_path, "result_rel_tag.xlsx")
#         df_input = PandaTool.read(input_data_path)
#         format_object.process(df_input)



class TestUnitRelationTag(unittest.TestCase):
    def test_ver_map(self):
        ver_object = VerMappingCollect(tag_config_path)
        if ver_object.ver_status:
            print("词表验证通过")
        else:
            print("Exception:{}".format(ver_object.ver_list))



if __name__ == '__main__':
    unittest.main()
