# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 
# author : 
# create_time : 2020/8/31 13:54
# update_time : 2020/8/31 13:54
# copyright : Lavector
# ----------------------------------------------
import os

from maxda.util.config_util import ConfigUtil
from maxda.executor.py_model_loader import PyModelLoader
from maxda.analysis.da_clean.clean_interface import *
from maxda.analysis.da_clean.df_distinct import DfDistinct
from maxda.analysis.da_filter.clean_filter import CleanFilter
from maxda.analysis.da_filter.column_match_filter import *
from maxda.analysis.da_pre.create_data_index import CreateDataIndex


class TaskParam(object):
    def __init__(self, input_column, output_column, processor, name=None):
        """

        :param input_column: None or list, 输入字段，适用于行接口
        :param output_column: None or list，输出字段，适用于行接口
        :param processor: object,功能处理类
        :param name:string, 名称
        """
        self._input_column = input_column
        self._output_column = output_column
        self._processor = processor
        if name is not None:
            self._name = name
        else:
            self._name = str(type(processor).__name__)

        # 输出结果文件名/可以是包括完整路径的文件名,适用于统计类接口
        self._output_file = None

        # 清洗策略
        self._filters = list()

    @property
    def name(self):
        return self._name

    @name.setter
    def filters(self, value):
        self._name = value

    @property
    def filters(self):
        return self._filters

    @filters.setter
    def filters(self, value):
        self._filters = value

    @property
    def output_file(self):
        return self._output_file

    @output_file.setter
    def output_file(self, value):
        self._output_file = value

    @property
    def input_column(self):
        return self._input_column

    @input_column.setter
    def input_column(self, value):
        self._input_column = value

    @property
    def output_column(self):
        return self._output_column

    @output_column.setter
    def output_column(self, value):
        self._output_column = value

    @property
    def processor(self):
        return self._processor

    @processor.setter
    def processor(self, value):
        self._processor = value


class ConfigLabel(object):
    """
    配置文件标签
    """
    # 类名
    CLASS = 'class'
    # 输入字段,暂时不用
    INPUT_COLUMN = "input_column"
    # 输出字段,暂时不用
    OUTPUT_COLUMN = "output_column"
    # 类初始化参数
    INIT = "init"
    # config 资源文件
    CONFIG = "config"
    # pair-name，输入输出字段名
    PAIR_COLUMN = 'pair_column'
    # 输出文件
    OUTPUT_FILE = 'output_file'
    # 过虑
    FILTER = "filter"


class TaskBuilder(object):
    def _parse_common_columns(self, col_str, default_value=None):
        if not col_str:
            return default_value
        tmp_list = re.split("[,，]", col_str)
        tmp_list = [item.strip() for item in tmp_list if item.strip()]
        if len(tmp_list) <= 0:
            return default_value

        return tmp_list

    def _build_row_task(self, item, class_object, run_params_dict, default_value=None):
        """
        构建行接口任务类
        :param item:
        :param class_object:
        :return:
        """

        # 1.构建输入、输出列名
        result_list = list()

        if ConfigLabel.INPUT_COLUMN in item or ConfigLabel.OUTPUT_COLUMN in item:
            input_column = None
            if ConfigLabel.INPUT_COLUMN in item:
                input_column = self._parse_common_columns(item[ConfigLabel.INPUT_COLUMN], default_value)
                if not input_column:
                    raise Exception("input columns has no data")
            output_column = None
            if ConfigLabel.OUTPUT_COLUMN in item:
                output_column = self._parse_common_columns(item[ConfigLabel.OUTPUT_COLUMN], default_value)
            if not output_column:
                raise Exception("output column is empty for class = " + item[ConfigLabel.CLASS])

            result_list.append((input_column, output_column))
            return result_list
        elif ConfigLabel.PAIR_COLUMN in item:
            tmp_list = re.split("[;；]", item[ConfigLabel.PAIR_COLUMN])
            tmp_list = [item.strip() for item in tmp_list if item.strip()]

            for sub_str in tmp_list:
                if "=" not in sub_str:
                    raise Exception("pair column must has '=' for class = " + item[ConfigLabel.CLASS])
                sub_list = sub_str.split("=")
                sub_list = [item.strip() for item in sub_list if item.strip()]

                if 2 < len(sub_list) or len(sub_list) <= 0:
                    raise Exception("invalid pair column =" + item[ConfigLabel.PAIR_COLUMN])

                if len(sub_list) == 2:
                    input_column = self._parse_common_columns(sub_list[0], default_value)
                    output_column = self._parse_common_columns(sub_list[1], default_value)

                    result_list.append((input_column, output_column))
                else:
                    if sub_str.startswith("="):
                        output_column = self._parse_common_columns(sub_list[0])
                        result_list.append((default_value, output_column))
                    else:
                        input_column = self._parse_common_columns(sub_list[0])
                        result_list.append((input_column, default_value))
                # 应该具有相同的输入，输出
                input_set = set()
                output_set = set()
                for tmp_col_item in result_list:
                    in_len = len(tmp_col_item[0]) if tmp_col_item[0] else 0
                    ou_len = len(tmp_col_item[1]) if tmp_col_item[1] else 0
                    input_set.add(in_len)
                    output_set.add(ou_len)

                if len(input_set) > 1:
                    raise Exception("pair must has same number of input column for class =" + item[ConfigLabel.CLASS])
                if len(output_set) > 1:
                    raise Exception("pair must has same number of output column for class =" + item[ConfigLabel.CLASS])
        else:
            raise Exception("has no input/output column")

        # 2.构建洗洗类
        filter_list = list()
        # 创建索引的功能不需要过虑功能
        if not isinstance(class_object, CreateDataIndex):
            # TODO 默认所有非清洗类行接口都要使用此策略
            if not isinstance(class_object, CleanInterface):
                if run_params_dict['userCleanFilter']:
                    filter_list.append(CleanFilter(run_params_dict['userCleanFilter']))

            if ConfigLabel.FILTER in item:
                filter_item = item[ConfigLabel.FILTER]
                for one_key in filter_item:
                    # TODO 暂时只定义的一种过虑策略
                    if one_key == "column_filter_not_match":
                        filter_list.append(ColumnNotMatchFilter(filter_item[one_key]))

        # 3.构建Task
        task_param_list = list()
        for one_result in result_list:
            one_task_param = TaskParam(one_result[0], one_result[1], class_object)
            one_task_param.filters = filter_list
            task_param_list.append(one_task_param)

        return task_param_list

    def make_task(self, config, config_data_path, run_params_dict):
        """
        校验任务参数并生成任务
        :param config:
        :return:
        """
        if isinstance(config, str):
            config_list = ConfigUtil.get_flow_config(config)
        elif isinstance(config, list):
            config_list = config
        else:
            raise Exception("unknown config data")

        if config_data_path is not None and not os.path.isdir(config_data_path):
            raise Exception("config path is not a dir!" + config_data_path)

        if len(config_list) <= 0:
            raise Exception("empty task config!")

        loader = PyModelLoader()
        task_param_list = list()
        for item in config_list:
            # 1.生成任务类
            if ConfigLabel.CLASS not in item:
                raise Exception("has not task class ")
            # TODO 是否为框架自动生成的类
            is_load_object = True
            if isinstance(item[ConfigLabel.CLASS], TaskInterface):
                class_object = item[ConfigLabel.CLASS]
                is_load_object = False
            else:
                int_dict = item[ConfigLabel.INIT] if ConfigLabel.INIT in item else None
                if int_dict:
                    class_object = loader.load(item[ConfigLabel.CLASS], **int_dict)
                else:
                    class_object = loader.load(item[ConfigLabel.CLASS])
            # 2.生成相应的数据字段
            default_column = None
            if isinstance(class_object, RowInterface):
                # 行接口为要解析输入、输出字段
                sub_task_list = self._build_row_task(item, class_object, run_params_dict, default_column)
                task_param_list.extend(sub_task_list)
            elif isinstance(class_object, DfProcessInterface):
                # DataFrame 任务生成类接口
                # TODO 去重类特殊处理
                # TODO 去重类实在是太特殊了，因此这里只能使用特例了
                if isinstance(class_object, DfDistinct):
                    distinct_init = item[ConfigLabel.INIT]
                    task_param_list.append(TaskParam([distinct_init['input_column']], [distinct_init['output_column']], class_object))
                else:
                    task_param_list.append(TaskParam(default_column, default_column, class_object))
            elif isinstance(class_object, DfStatisInterface):
                # 统计类接口要有输出结果文件名
                if ConfigLabel.OUTPUT_FILE not in item:
                    raise Exception("统计类接口需要包含output_file字段")
                one_task_param = TaskParam(default_column, default_column, class_object)
                one_task_param.output_file = item[ConfigLabel.OUTPUT_FILE]

                task_param_list.append(one_task_param)
            elif isinstance(class_object, DfMergeInterface):
                one_task_param = TaskParam(default_column, default_column, class_object)
                task_param_list.append(one_task_param)
            else:
                raise Exception("unknown interface for class = " + str(type(class_object).__name__))

            # 3.初始化配置资源
            # TODO 用户自己初始化的功能，暂时不再加载资源了
            if is_load_object:
                if ConfigLabel.CONFIG in item:
                    config_dict = item[ConfigLabel.CONFIG]
                    # 校验文件
                    for one_key in config_dict:
                        one_value = config_dict[one_key]
                        if not os.path.isfile(one_key):
                            one_value = os.path.join(config_data_path, one_value)
                            config_dict[one_key] = one_value
                        # if not os.path.exists(one_value):
                        #     raise Exception("config file not exist = " + one_value)
                    class_object.load_config_data(**config_dict)

        return task_param_list

    def split(self, task_param_list):
        """
        拆分task，分为一般Task和数据合并task
        :param task_param_list:
        :return:
        """
        if isinstance(task_param_list[0].processor, DfMergeInterface):
            task_merge = task_param_list[0]
            if len(task_param_list) > 1:
                task_other = task_param_list[1:]
            else:
                task_other = list()
        else:
            task_merge = None
            task_other = task_param_list

        # TODO 校验任务，只有特定接口的功能类可以作为任务流使用
        for task_param in task_other:
            if isinstance(task_param.processor, TaskInterface):
                continue
            raise Exception("unsupport task type for" + str(type(task_param.processor).__name__))

        return [task_merge, task_other]

    def make_task_meta(self, task_param_list):
        """
        构建一下运行时的任务数据，以方便其他功能舍不得，如清洗
        :param task_param_list:
        :return:
        """
        meta_dict = dict()
        # 获取所有清洗数据的输出字段
        meta_dict['cleanOutput'] = list()
        for param_object in task_param_list:
            if isinstance(param_object.processor,  CleanInterface):
                if param_object.output_column:
                    meta_dict['cleanOutput'].extend(param_object.output_column)

        # 获取所有任务数量
        meta_dict['taskCount'] = len(task_param_list)
        row_task_count = 0
        df_process_count = 0
        df_statis_count = 0
        df_merge_count = 0
        for task_param_object in task_param_list:
            if isinstance(task_param_object.processor, DfProcessInterface):
                df_process_count += 1
            elif isinstance(task_param_object.processor, RowInterface):
                row_task_count += 1
            elif isinstance(task_param_object.processor, DfStatisInterface):
                df_statis_count += 1
            elif isinstance(task_param_object.processor, DfMergeInterface):
                df_merge_count += 1

        meta_dict['rowTaskCount'] = row_task_count
        meta_dict['dfProcessTaskCount'] = df_process_count
        meta_dict['dfStatisTaskCount'] = df_statis_count
        meta_dict['dfMergeTaskCount'] = df_merge_count

        return meta_dict

    def build(self, config, config_data_path, run_params_dict):
        task_param_list = self.make_task(config, config_data_path, run_params_dict)
        split_result = self.split(task_param_list)

        meta_dict = self.make_task_meta(task_param_list)

        return split_result + [meta_dict]