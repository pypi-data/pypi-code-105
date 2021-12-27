# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 测试处理流框架
# author : 
# create_time : 2020/7/30 11:57
# update_time : 2020/7/30 11:57
# copyright : Lavector
# ----------------------------------------------
import unittest

from dataset.dataset_config import *
from maxda.executor.df_executor import DfExecutor
from maxda.util.config_util import ConfigUtil


class TestFlow(unittest.TestCase):
    def test_df_flow(self):
        # 测试核心处理功能

        core_flow_path = os.path.join(example_config_path, "da_all_flow.xml")
        # TODO 不要数据合并功能
        core_flow = ConfigUtil.get_flow_config(core_flow_path)
        core_flow = [item for item in core_flow if item['id'] not in {"315", '316', '602'}]

        # 删除数据合并功能
        core_flow = core_flow[1:]
        input_file_path = os.path.join(example_test_input_path, "data_merge.xlsx")
        executor = DfExecutor()
        executor.run_flow(config_flow=core_flow,
                          input_source=input_file_path,
                          config_path=example_config_path,
                          output_source=None,
                          statis_output_path=None)


if __name__ == "__main__":
    flow = TestFlow()
    flow.test_df_flow()


