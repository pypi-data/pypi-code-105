# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 
# author : 
# create_time : 2020/9/8 13:45
# update_time : 2020/9/8 13:45
# copyright : Lavector
# ----------------------------------------------
import pandas as pd

from maxda.util.panda_tool import PandaTool
from maxda.util.file_tool import FileTool


class HiveSource(object):
    def __init__(self, table_name):
        self._table_name = table_name

    @property
    def table_name(self):
        return self._table_name


class DaDataLoader(object):
    @staticmethod
    def load_from_file(input_path, merge_task_object=None, suffix=".xlsx"):
        """
        加载数据
        :param input_path:string, 目录/文件
        :param merge_task_object:object, 数据合并类
        :return:
        """
        # 1.获取所有数据文件路径
        if isinstance(input_path, (list, tuple, set)):
            file_params_list = input_path
        else:
            file_params_list = FileTool.get_file_path(input_path, suffix=".xlsx")
            if not file_params_list:
                return None
        if len(file_params_list) <= 0:
            raise Exception("no data input")

        # 2.加载数据
        if merge_task_object is not None:
            df_data = merge_task_object.processor.process(file_params_list)
        else:
            df_list = list()
            for file_path in file_params_list:
                df_one = PandaTool.read_more(file_path)
                df_list.append(df_one)

            df_data = pd.concat(df_list, sort=False)

        return df_data
