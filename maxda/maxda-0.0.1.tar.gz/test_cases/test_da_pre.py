# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 测试预处理相关功能
# author : 
# create_time : 2020/7/18 16:00
# update_time : 2020/7/18 16:00
# copyright : Lavector
# ----------------------------------------------
import unittest

from dataset.dataset_config import *
from maxda.analysis.da_pre.df_format_data import *


class TestUnitPre(unittest.TestCase):
    def test_merge(self):
        format_object = DfFormatData()
        file_path = [os.path.join(example_input_path, "data_redbook.xlsx"),
                     os.path.join(example_input_path, "data_tmall.xlsx"),
                     os.path.join(example_input_path, "data_weibo.xlsx")
                     ]
        format_object.process(file_path)


if __name__ == '__main__':
    unittest.main()
