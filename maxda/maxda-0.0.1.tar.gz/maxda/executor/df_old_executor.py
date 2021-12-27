# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 基于DataFrame的处理框架
# author : 
# create_time : 2020/6/30 16:06
# update_time : 2020/6/30 16:06
# copyright : Lavector
# ----------------------------------------------
import pandas as pd
import os
import math
from joblib import Parallel, delayed
import threading
from datetime import datetime

from maxda.util.panda_tool import PandaTool
from maxda.util.file_tool import FileTool
from maxda.util.time_util import TimeTool
from maxda.analysis.da_clean.clean_interface import *
from maxda.executor.task import *


def gl_process_line_fun(task_param_object, line_data, task_meta):
    """
    全局通用处理函数，处理一行数据
    :param task_param_object:
    :param line_data: dict, 一行数据
    :return:
    """
    # 1.filter 检查
    if task_param_object.filters:
        for filter_object in task_param_object.filters:
            if filter_object.process((line_data, task_meta)):
                return task_param_object.processor.get_default_value()

    # 2.筛选需要的数据
    # TODO 不指定输入列时返回全部
    if task_param_object.input_column is None or len(task_param_object.input_column) <= 0:
        sel_line_data = line_data
    elif len(task_param_object.input_column) == 1:
        # TODO 只有一个字段时，返回非集合数据
        sel_line_data = line_data[task_param_object.input_column[0]]
    else:
        sel_line_data = {key: line_data[key] for key in task_param_object.input_column}

    # 3.处理数据
    result = task_param_object.processor.process(sel_line_data)

    return result


def gl_process_batch_fun(task_param_object, batch_data_list, task_meta):
    batch_result_list = [gl_process_line_fun(task_param_object, line_data, task_meta) for line_data in batch_data_list]
    return batch_result_list


def gl_process_threading_fun(task_param_object, batch_data_list, task_meta, result_list):
    batch_result_list = gl_process_batch_fun(task_param_object, batch_data_list, task_meta)
    for i, line_result in enumerate(batch_result_list):
        result_list[i] = line_result


def gl_clean_line_dict(line_dict):
    """
    主要是清理空数据
    :param line_dict:
    :return:
    """
    line_dict = {key: line_dict[key] if not pd.isna(line_dict[key]) and line_dict[key] != "" else None for key in line_dict}

    return line_dict


def gl_format_df_data(df_input):
    """
    格式化dataframe 数据为python list
    因为DataFrame的遍历操作好像比较慢，不如list快
    :param df_input:
    :return:
    """
    data_list = df_input.to_dict(orient="records")
    data_list = [gl_clean_line_dict(item) for item in data_list]

    return data_list


class DfOldExecutor(object):
    """
    基于DataFrame的数据处理框架
    """
    def __init__(self, max_lines=700000, jobs=1, mode=0, job_batch_size=1000, channel_col="channel"):
        """

        :param max_lines: int, 单个文件保存的最大数据量(行数)
        :param jobs:  并行数量
        :param mode: int, 并行工作模式, jobs> 1时有作用,
                    0:joblib 多进程，
                    1:joblib 多线程，
                    3:threading 多线程，
        :param job_batch_size: int, mode=0时，单个job 单批处理的最大数据量
        :param channel_col: string, string,channel字段名
        """
        self.max_lines = max_lines
        self.jobs = jobs
        self.mode = mode
        self.job_batch_size = job_batch_size

        # TODO flow、task 相关配置及运行数据
        self._task_meta = None
        self.channel_col = channel_col

    def get_task_meta(self):
        return self._task_meta

    def load_data(self, input_path, merge_task_object=None, suffix=".xlsx"):
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

    def _count_data_meta(self, df_input):
        """
        统计输入数据相关内容
        :param df_input:
        :return:
        """
        data_meta = dict()
        data_meta['count'] = df_input.shape[0]
        data_meta['fieldCount'] = df_input.shape[1]

        # if self.channel_col in set(df_input.columns):
        #     df_channel_count = df_input.groupby(['channel']).agg({"channel": 'count'})
        #     df_channel_count.rename(columns={'channel': 'count'},
        #                             inplace=True)
        #     df_channel_count = df_channel_count.reset_index(drop=False)
        #     channel_meta = df_channel_count.to_dict(orient="records")
        #     data_meta['channel'] = channel_meta

        return data_meta

    def run_flow(self, config_flow,
                 input_path,
                 config_path,
                 output_path=None,
                 statis_output_path=None,
                 suffix=".xlsx",
                 clean_result_prefix="tag_clean_"):
        """
        运行数据处理任务流
        :param config_flow: string or dict,配置文件或配置数据
                            (1) string:任务流配置文件
                            (2) dict：基于配置文件解析出来的任务流数据
        :param input_path: string, 输入数据, 可选值:
                                （1）文件目录： 此目录中所有的以suffix为后缀的文件都作为输入数据
                                 (2) 文件（須包含完整的路径）：单个文件作为数据
                                 (3) 文件列表（须包含完整的路径）：list/tuple(文件)
        :param config_path: string, 配置数据目录, 必须是已经存在的目录
                             此目录用以存放各个Task所需要的资源，
        :param output_path: string,数据处理结果文件名,必须是包含完整路径的文件名
                         当最后处理结果一个文件存不下时，必自动存储为多个文件
                         以输入的文件名作为前缀
                         eg: /Download/output.xlsx, 实际结果可以为 output_1.xlsx, output_2.xlsx
        :param statis_output_path: 统计类结果存储目录，目录不存在则自动构建
        :param suffix: string,input_data_path 输入数据的后缀
        :param jobs:  并行数量
        :param mode: int, 并行工作模式, jobs> 1时有作用,
                    0:多进程，
                    1:多线程，
        :param clean_result_prefix:  string or None
                                   string: 是否对所有行处理功能(不包括清洗功能、创建过些功能)过虑清洗掉的数据
                                   None: 不过虑清洗的数据
        """
        # 0.校验输出目录
        if statis_output_path is not None:
            FileTool.make_dir(statis_output_path)
        run_params_dict = dict()
        run_params_dict['userCleanFilter'] = clean_result_prefix

        # 1.构建Task
        task_builder = TaskBuilder()
        task_merge_object, task_other_list, task_meta = task_builder.build(config_flow, config_path, run_params_dict)
        self._task_meta = task_meta
        # 2.加载数据
        df_input = self.load_data(input_path, merge_task_object=task_merge_object, suffix=suffix)
        task_meta['data'] = self._count_data_meta(df_input)

        # 3.运行任务
        df_result = self._run_process(df_input, task_other_list, task_meta, statis_output_path, self.jobs, self.mode)

        # 4.保存数据
        # 只有统计类结果时，不需要再保存原始数据，因此没有数据更改
        if output_path is not None and task_meta['taskCount'] != task_meta['dfStatisTaskCount']:
            output_dir = FileTool.get_parent_dir(output_path)
            FileTool.make_dir(output_dir)
            PandaTool.save(output_path, df_result, max_line=self.max_lines)

        return df_result

    def _run_process(self, df_input, task_param_list, task_meta, statis_output_path, jobs, mode):
        """
        核心运行代码
        :param df_input:DataFrame，待处理数据
        :param task_param_list:list(TaskParam)，任务列表
        :param statis_output_path:string，统计类Task结果输出目录
        :return:
        """
        task_time_list = list()
        for task_param_object in task_param_list:
            # TODO 统计各任务执行时间
            begin_time = datetime.now()
            # 行接口可以并行处理
            if isinstance(task_param_object.processor, RowInterface):
                # TODO 校验输入，输入字段不存在则不执行此任务
                skip = False
                if task_param_object.input_column:
                    cur_column = set(PandaTool.get_column(df_input))
                    for col in task_param_object.input_column:
                        if col not in cur_column:
                            skip = True
                            break
                if skip:
                    continue

                # 实际执行处理任务
                if jobs > 1:
                    all_line_result = self._parallel_row_process(df_input, task_param_object, task_meta, jobs, mode)
                else:
                    all_line_result = self._single_row_process(df_input, task_param_object, task_meta)

                # 处理结果添加到原有数据集上
                output_column = task_param_object.output_column
                if len(output_column) == 1:
                    df_input[output_column[0]] = all_line_result
                else:
                    for i, one_column in enumerate(output_column):
                        one_column_result = [item[i] for item in all_line_result]
                        df_input[one_column] = one_column_result
            elif isinstance(task_param_object.processor, DfProcessInterface):
                # 基于DataFrame处理数据，单独处理
                df_input = task_param_object.processor.process(df_input)
            elif isinstance(task_param_object.processor, DfStatisInterface):
                # 统计功能，不改变原数据
                # TODO 现有统计功能可能会修改原数据，因此要复制一份吧，虽然会比较费时，但也没办法了
                df_statis_input = df_input.copy(deep=True)
                df_statis_result = task_param_object.processor.process(df_statis_input)
                del df_statis_input

                s_output_file = task_param_object.output_file
                # 有分隔符代表可能是全路径，没有的只是文件名
                if statis_output_path is not None:
                    if os.sep not in s_output_file:
                        s_output_file = os.path.join(statis_output_path, s_output_file)
                    if isinstance(df_statis_result, dict):
                        PandaTool.save_many(s_output_file, df_statis_result, index=True)
                    else:
                        PandaTool.save(s_output_file, df_statis_result, max_line=self.max_lines, index=True)

            end_time = datetime.now()
            run_time = TimeTool.epoch_seconds(begin_time, end_time)
            one_task_time = dict()
            one_task_time['start'] = begin_time.strftime('%Y-%m-%d %H:%M:%S')
            one_task_time['end'] = end_time.strftime('%Y-%m-%d %H:%M:%S')
            one_task_time['runTime'] = round(float(run_time), 3)
            one_task_time['class'] = task_param_object.name
            one_task_time['inputColumn'] = task_param_object.input_column

            task_time_list.append(one_task_time)

        task_meta['taskTime'] = task_time_list

        return df_input

    def _single_row_process(self, df_input, task_param_object, task_meta):
        """
        串行数据处理
        :param df_input: DataFrame，待处理数据
        :param task_param_object: list(TaskParam)，任务列表
        :param task_meta: dict,任务元数据
        :return:
        """
        data_list = gl_format_df_data(df_input)
        all_line_result = [gl_process_line_fun(task_param_object,
                                               line_data,
                                               task_meta) for line_data in data_list]

        return all_line_result

    def split_df(self, df_input, batch_size):
        total_data_count = df_input.shape[0]

        total_batch_list = list()
        start = 0
        while start < total_data_count:
            end = start + batch_size
            if end >= total_data_count:
                one_batch = df_input.iloc[start:]
                start = total_data_count
            else:
                one_batch = df_input.iloc[start: end]
                start = end
            total_batch_list.append(one_batch)

        return total_batch_list

    def split_by_batch(self, total_data_list, batch_size):
        total_data_count = len(total_data_list)

        total_batch_list = list()
        start = 0
        while start < total_data_count:
            end = start + batch_size
            if end >= total_data_count:
                one_batch = total_data_list[start:]
                start = total_data_count
            else:
                one_batch = total_data_list[start: end]
                start = end
            total_batch_list.append(one_batch)

        return total_batch_list

    def split_by_task(self, total_data_list, task_count):
        total_data_count = len(total_data_list)
        if total_data_count < task_count:
            task_count = len(total_data_list)

        batch_size = int(math.ceil(total_data_count / float(task_count)))
        total_batch_list = list()
        start = 0
        while start < total_data_count:
            end = start + batch_size
            if end >= total_data_count:
                one_batch = total_data_list[start:]
                start = total_data_count
            else:
                one_batch = total_data_list[start: end]
                start = end
            total_batch_list.append(one_batch)

        return total_batch_list

    def _parallel_row_process(self, df_input, task_param_object, task_meta, jobs, mode):
        """
        并行数据处理
        :param df_input: DataFrame，待处理数据
        :param task_param_object:list(TaskParam)，任务列表
        :param jobs: int，并发数量
        :param mode: int，并发模式
        :return:
        """
        input_data_list = gl_format_df_data(df_input)

        if mode == 0:
            all_batch_list = self.split_by_batch(input_data_list, self.job_batch_size)
            all_batch_result = Parallel(n_jobs=jobs)(
                delayed(gl_process_batch_fun)(task_param_object,
                                              one_batch,
                                              task_meta)
                for one_batch in all_batch_list)

            all_line_result = list()
            for on_batch_result in all_batch_result:
                all_line_result.extend(on_batch_result)

        elif mode == 1:
            all_line_result = Parallel(n_jobs=jobs, backend="threading")(
                delayed(gl_process_line_fun)(task_param_object,
                                             line_data,
                                             task_meta)
                for line_data
                in
                input_data_list)
        elif mode == 3:
            all_batch_list = self.split_by_task(input_data_list, jobs)
            jobs = len(all_batch_list)
            all_thread_result = list()
            thread_list = list()
            for i in range(jobs):
                one_batch_result = [None for _ in range(len(all_batch_list[i]))]
                all_thread_result.append(one_batch_result)
                t = threading.Thread(target=gl_process_threading_fun, args=(task_param_object,
                                                                            all_batch_list[i],
                                                                            task_meta,
                                                                            one_batch_result))
                # t.setDaemon(True)
                t.start()
                thread_list.append(t)

            for t in thread_list:
                t.join()

            all_line_result = list()
            for on_batch_result in all_thread_result:
                all_line_result.extend(on_batch_result)
        else:
            raise Exception("unknow mode = " + str(mode))

        return all_line_result










