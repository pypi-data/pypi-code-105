# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 测试统计类相关功能
# author : 
# create_time : 2020/7/18 16:04
# update_time : 2020/7/18 16:04
# copyright : Lavector
# ----------------------------------------------
import unittest

from maxda.analysis.da_statis.da_qa_class import *
from maxda.util.panda_tool import PandaTool
from dataset.dataset_config import *



data_path = os.path.join(example_test_input_path, "data_statis.xlsx")
df_statis = PandaTool.read(data_path)


class TestUnitStatis(unittest.TestCase):
    def test_pre(self):
        pre_object = PreQuality(index_column="da_index", input_column_str="age,gender")
        pre_object.process(df_statis)

    def test_statis_clean(self):
        clean_object = CleanQuality()
        clean_object.process(df_statis)

    def test_statis_tag(self):
        clean_object = TagQuality(index_column="da_index", input_column_prefix="tag_format")
        clean_object.process(df_statis)


if __name__ == '__main__':
    unittest.main()