# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 
# author : 
# create_time : 2020/8/31 17:51
# update_time : 2020/8/31 17:51
# copyright : Lavector
# ----------------------------------------------
import pandas as pd
import math
from joblib import Parallel, delayed
import threading
from datetime import datetime

from maxda.util.panda_tool import PandaTool
from maxda.util.file_tool import FileTool
from maxda.util.time_util import TimeTool
from maxda.executor.data_loader import DaDataLoader
from maxda.analysis.da_clean.clean_interface import *
from maxda.executor.task import *
from maxda.executor.base_executor import BaseExecutor, gl_process_line_fun, gl_clean_line_dict
from maxda.util.py_thread import PyThread


def gl_process_batch_fun(task_param_object, batch_data_list, task_meta):
    batch_result_list = [gl_process_line_fun(task_param_object, line_data, task_meta) for line_data in batch_data_list]
    return batch_result_list


def gl_process_threading_fun(task_param_object, batch_data_list, task_meta, result_list):
    batch_result_list = gl_process_batch_fun(task_param_object, batch_data_list, task_meta)
    for i, line_result in enumerate(batch_result_list):
        result_list[i] = line_result


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


class DfExecutor(BaseExecutor):
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
        super(DfExecutor, self).__init__(channel_col, max_lines)

        self.max_lines = max_lines
        self.jobs = jobs
        self.mode = mode
        self.job_batch_size = job_batch_size

    def run_process(self, df_input, task_param_list, task_meta, statis_output_path, params=None):
        """
        核心运行代码
        :param df_input:DataFrame，待处理数据
        :param task_param_list:list(TaskParam)，任务列表
        :param statis_output_path:string，统计类Task结果输出目录
        :param params:dict，运行参数
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
                # 处理行功能
                df_input = self.run_row_task(df_input, task_param_object, task_meta)

            else:
                df_input = self.process_df_task(df_input, task_param_object, statis_output_path)

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

    def count_data_meta(self, df_input):
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

    def load_data(self, data_source, merge_task_object, suffix, task_meta):
        df_input = DaDataLoader.load_from_file(data_source, merge_task_object, suffix)
        task_meta['data'] = self.count_data_meta(df_input)

        return df_input

    def save_result(self, df_result, task_meta, output_source=None):
        if output_source is not None and task_meta['taskCount'] != task_meta['dfStatisTaskCount']:
            if df_result is not None:
                output_dir = FileTool.get_parent_dir(output_source)
                FileTool.make_dir(output_dir)
                PandaTool.save(output_source, df_result, max_line=self.max_lines)

    def run_row_task(self, df_input, task_param_object, task_meta):
        # 实际执行处理任务
        if self.jobs > 1:
            all_line_result = self._parallel_row_process(df_input, task_param_object, task_meta, self.jobs, self.mode)
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
        # 测试使用
        # all_line_result = list()
        # count = 0
        # start_time = datetime.now()
        # t_list = list()
        # for i, line_data in enumerate(data_list):
        #     count += 1
        #
        #     t_list.append(len(line_data['content']))
        #     if count % 5 == 0:
        #
        #         end_time = datetime.now()
        #         epoch_time = TimeTool.epoch_seconds(start_time, end_time)
        #         start_time = end_time
        #         avg_len = float(sum(t_list)) / len(t_list)
        #         print(count, line_data['channel'], epoch_time, avg_len, t_list)
        #
        #         t_list = list()
        #     line_result = gl_process_line_fun(task_param_object,
        #                                         line_data,
        #                                         task_meta)
        #     all_line_result.append(line_result)

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
                # TODO 由于默认线程类的异常无法被主线程捕捉，因此使用自定义的线程类
                # t = threading.Thread(target=gl_process_threading_fun, args=(task_param_object,
                #                                                             all_batch_list[i],
                #                                                             task_meta,
                #                                                             one_batch_result))

                t = PyThread(target=gl_process_threading_fun, args=(task_param_object,
                                                                    all_batch_list[i],
                                                                    task_meta,
                                                                     one_batch_result))
                # t.setDaemon(True)
                t.start()
                thread_list.append(t)

            for t in thread_list:
                t.join()

            # TODO 检查线程状态
            for t in thread_list:
                if t.exit_code != 0:
                    raise Exception("df executor thread exception:" + t.exc_traceback)

            all_line_result = list()
            for on_batch_result in all_thread_result:
                all_line_result.extend(on_batch_result)
        else:
            raise Exception("unknow mode = " + str(mode))

        return all_line_result
