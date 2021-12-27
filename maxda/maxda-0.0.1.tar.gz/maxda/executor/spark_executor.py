# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 
# author : 
# create_time : 2020/8/31 18:16
# update_time : 2020/8/31 18:16
# copyright : Lavector
# ----------------------------------------------
# from pyspark.sql import SparkSession
import pandas as pd
from pyspark.sql import HiveContext

from maxda.util.panda_tool import PandaTool
from maxda.util.file_tool import FileTool
from maxda.analysis.analysis_interface import *
from maxda.executor.data_loader import HiveSource
from maxda.executor.data_loader import DaDataLoader
from maxda.executor.base_executor import BaseExecutor, gl_process_line_fun, gl_clean_line_dict


def format_spark_result(result, default_value=""):
    """
    格式化结果，结果全部转为字符串类型
    :param result: Processor 处理的结果
    :param default_value: 默认值
    :return:
    """
    if result is None:
        return default_value
    return str(result)


def gl_do_process_spark_line(task_param_list, line_data, task_meta):
    # 1.格式化数据
    data = line_data.asDict()
    line_data = gl_clean_line_dict(data)

    # 2. 各个task按顺序执行
    for task_param_object in task_param_list:
        # 2.处理数据
        line_result = gl_process_line_fun(task_param_object, line_data, task_meta)

        # 3.返回结果添加新字段
        # 处理结果添加到原有数据集上
        output_column = task_param_object.output_column
        if len(output_column) == 1:
            line_data[output_column[0]] = format_spark_result(line_result)
        else:
            for i, one_column in enumerate(output_column):
                line_data[one_column] = format_spark_result(line_result[i])

    return line_data


class SparkExecutor(BaseExecutor):
    def __init__(self, spark_session,
                 tmp_hive_table,
                 max_lines=700000,
                 channel_col="channel"
                 ):
        """

        :param spark_session:
        :param tmp_hive_table: string, hive临时表，必须是包含数据库的完整名称，当数据源是文件时，需要将数据存入临时hive表以便spark处理
        :param max_lines:
        :param channel_col:
        """
        super(SparkExecutor, self).__init__(channel_col, max_lines)
        self.spark_session = spark_session
        self.tmp_hive_table = tmp_hive_table

        self.hive_ctx = HiveContext(self.spark_session.sparkContext)

    def load_data(self, input_source, merge_task_object, suffix, task_meta):
        if isinstance(input_source, HiveSource):
            spark_input_df = self.get_from_hive(input_source.table_name)
        else:
            df_input = DaDataLoader.load_from_file(input_source, merge_task_object, suffix)
            if task_meta['rowTaskCount'] > 0:
                # TODO 没有行任务时，不需要转为Spar kDataFrame
                self.save_to_hive(df_input, self.tmp_hive_table)
                spark_input_df = self.get_from_hive(self.tmp_hive_table)
            else:
                spark_input_df = df_input

        return spark_input_df

    def run_process(self, df_input, task_param_list, task_meta, statis_output_path, params=None):
        """
        核心运行代码
        :param df_input:Spark DataFrame 或 pandas DataFrame，待处理数据
        :param task_param_list:list(TaskParam)，任务列表
        :param task_meta:dict，任务元数据
        :param statis_output_path:string，统计类Task结果输出目录
        :return:
        """
        task_row_list = list()
        task_other_list = list()

        # 1.拆分任务
        # df_input_col_set = set(list(df_input.columns))
        for task_param_object in task_param_list:

            # 行接口可以并行处理
            if isinstance(task_param_object.processor, RowInterface):
                # # TODO 校验输入，输入字段不存在则不执行此任务
                # skip = False
                # if task_param_object.input_column:
                #     cur_column = df_input_col_set
                #     for col in task_param_object.input_column:
                #         if col not in cur_column:
                #             skip = True
                #             break
                # if skip:
                #     continue
                # 处理行功能
                task_row_list.append(task_param_object)
            elif isinstance(task_param_object.processor, DfProcessInterface):
                task_other_list.append(task_param_object)
                # 基于DataFrame处理数据，单独处理
                # df_input = task_param_object.processor.process(df_input)
                # raise Exception("spark executor unsupport common DfProcess = ", str(type(task_param_object.processor).__name__))
            elif isinstance(task_param_object.processor, DfStatisInterface):
                task_other_list.append(task_param_object)
        if len(task_row_list) > 0:
            # 2. 数据先存入hive
            # print("------------first to hive-------------")
            spark_input_df = df_input

            # 3.先处理行功能
            # print("--------------spark process-----------")
            spark_result_rdd = self.run_row_task(spark_input_df, task_row_list, task_meta)

            # 4.数据格式转换
            # print("------------rdd tod spark dataframe-------------")
            spark_result_df = self.hive_ctx.createDataFrame(spark_result_rdd)

            # 5.数据格式转换,实际启动处理数据
            # print("------------to pandas -------------")
            df_result = spark_result_df.toPandas()
        else:
            df_result = df_input

        # 6.处理其他非spark可以处理的任务
        for task_param_object in task_other_list:
            df_result = self.process_df_task(df_result, task_param_object, statis_output_path)

        return df_result

    def save_result(self, df_result, task_meta, output_source=None):
        """
        保存处理结果,spark 真正开始处理的地方
        :param df_result: object, 数据处理结果
        :param task_meta: dict,元数据
        :param output_source: object
        :return:
        """
        if isinstance(output_source, HiveSource):
            # print("-------second to hive------------------------")
            if df_result is not None:
                self.save_to_hive(df_result, output_source.table_name)
        else:
            # 5.返回Pandas DataFrame结果
            # print("--------------save pandas df---------")
            if output_source is not None and task_meta['taskCount'] != task_meta['dfStatisTaskCount']:
                if df_result is not None:
                    output_dir = FileTool.get_parent_dir(output_source)
                    FileTool.make_dir(output_dir)
                    PandaTool.save(output_source, df_result, max_line=self.max_lines)

    def drop_table(self, full_table_name):
        self.hive_ctx.sql("drop table if exists {}".format(full_table_name))

    def get_from_hive(self, table_name):
        spark_df = self.hive_ctx.sql("select * from {}".format(table_name))

        return spark_df

    def save_to_hive(self, df_input, full_table_name, drop_if_exist=True):
        """
        将dataframe 数据存入hive
        :param df_input: python Dataframe
        :param full_table_name: string,完整的表名
        :param drop_if_exist: bool,是否删除原表
        :return:返回全部数据
        """
        if isinstance(df_input, pd.DataFrame):
            df_1 = self.hive_ctx.createDataFrame(df_input)
        else:
            df_1 = df_input

        # if drop_if_exist:
        #    self.drop_table(full_table_name)

        # TODO 覆盖历史数据
        df_1.write.saveAsTable(full_table_name, mode="overwrite")

    def run_row_task(self, spark_df, task_param_object_list, task_meta):
        """
        使用spark 运行基于行接口的任务
        :param spark_df: spark DataFrame
        :param task_param_object_list:
        :param task_meta:
        :return:
        """
        sc_task_param_list = self.spark_session.sparkContext.broadcast(task_param_object_list)
        sc_task_meta = self.spark_session.sparkContext.broadcast(task_meta)

        # if str(type(input_data).__name__) != "pyspark.sql.dataframe.DataFrame":
        #     spark_df = self.spark_session.createDataFrame(input_data)
        # else:
        #     spark_df = input_data

        # 类型：RDD
        spark_rdd = spark_df.rdd.map(lambda r: gl_do_process_spark_line(sc_task_param_list.value, r, sc_task_meta.value))

        return spark_rdd
