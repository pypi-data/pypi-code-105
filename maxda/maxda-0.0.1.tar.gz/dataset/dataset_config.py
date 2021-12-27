# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 
# author : 
# create_time : 2020/7/9 17:07
# update_time : 2020/7/9 17:07
# copyright : Lavector
# ----------------------------------------------
import os


def get_test_data_path():
    cur_cwd = os.getcwd()
    dir_name = "dataset"
    may_path_list = [os.path.join(cur_cwd, dir_name),
                     os.path.join(cur_cwd, '../'+dir_name),
                     os.path.join(cur_cwd, '../../' + dir_name)
                     ]

    for path in may_path_list:
        if os.path.exists(path):
            return path
    raise Exception("can not find test data root path!")


example_work_dir = get_test_data_path()


example_input_path = os.path.join(example_work_dir, "input_path")
example_config_path = os.path.join(example_work_dir, "config_path")
example_output_path = os.path.join(example_work_dir, "output_path")
example_statis_path = os.path.join(example_work_dir, "statis_path")

example_test_input_path = os.path.join(example_work_dir, "input_test_path")

example_merge_output_file = os.path.join(example_output_path, "data_merge.xlsx")

example_mine_path = os.path.join(example_work_dir, "mine_path")