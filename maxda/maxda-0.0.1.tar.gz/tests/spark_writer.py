# -*- coding:utf-8 -*-
# import findspark
# findspark.init()
import os
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import HiveContext, SparkSession
import pandas as pd
from middleware.utils import get_dir_files

input_path = "/home/wac/hanaojian/maxda-dev-spark/data"
project_id = 'kh_2020-09-02'

# global path_root, path_project
# path_root = os.getcwd()
# path_project = os.path.join(path_root, "data/run_project")
# input_data_path = os.path.join(path_project, "1_log")

def mergefile(input_path_1, project_id):
    print(input_path_1)
    files_path = get_dir_files(input_path_1, [], status=-1, str1=".DS_Store")
    print(files_path)
    df_list = []
    for infile in files_path:
        df = pd.read_excel(infile, header=0, error_bad_lines=False, encoding="utf_8_sig",dtype='str').fillna("")
        df_list.append(df)
    data_pd = pd.concat(df_list)
    data_pd['project_id'] = project_id

    return data_pd


def main():
    conf = SparkConf().setAppName('savepyspark').setMaster('local[*]')
    sc = SparkContext(conf = conf)
    sqlContext = HiveContext(sc)

    data_pd = mergefile(input_path,project_id)
    df_1 = sqlContext.createDataFrame(data_pd)

    df_1.write.saveAsTable('test.test_spark_data', mode='append', partitionBy=['project_id'])

    sc.stop()


if __name__ == '__main__':
    main()