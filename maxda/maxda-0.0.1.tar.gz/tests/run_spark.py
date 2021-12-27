# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 
# author : 
# create_time : 2020/9/1 10:18
# update_time : 2020/9/1 10:18
# copyright : Lavector
# ----------------------------------------------
import sys
sys.path.append("./")
sys.path.append("../")
sys.path.append(u'../')
sys.path.append(u'../../')
import os
from pyspark.sql import SparkSession, HiveContext
# from pyspark import SparkConf, SparkContext
from maxda.util.config_util import ConfigUtil
from maxda.executor.spark_executor import SparkExecutor
from maxda.util.panda_tool import PandaTool


def test_spark_flow(gl_spark):
    # 测试核心处理功能
    root_path = "/home/wac/liuguodong/data/spark_data"
    config_path = os.path.join(root_path, "config_path")
    input_path = os.path.join(root_path, "input_test_path")
    output_path = os.path.join(root_path, "output_path")
    core_flow_path = os.path.join(config_path,  "da_all_flow.xml")
    # TODO 不要数据合并功能
    core_flow = ConfigUtil.get_flow_config(core_flow_path)
    # 删除数据合并功能
    core_flow = core_flow[1:]

    core_flow = [item for item in core_flow if item['class'] in ["AgeFormat"]]  # "TagDealRelationSimple" "CustomCityRank" AgeFormat
    input_file_path = os.path.join(input_path, "data_merge.xlsx")

    result_file_path = os.path.join(output_path, 'maxda_result.xlsx')

    executor = SparkExecutor(gl_spark, tmp_hive_table="da_tmp.my_test")
    df_result = executor.run_flow(config_flow=core_flow,
                                  input_source=input_file_path,
                                  config_path=config_path,
                                  output_source=result_file_path,
                                  statis_output_path=None)
    # print(df_result['city'].tolist())
    # task_meta = executor.task_meta
    # print(task_meta)


def run_save_hive(gl_spark):
    hiveCtx = HiveContext(gl_spark.sparkContext)

    root_path = "/home/wac/liuguodong/data/spark_data"
    input_file_path = os.path.join(root_path, *["input_test_path", "data_merge.xlsx"])

    data_pd = PandaTool.read(input_file_path)
    print("shape =", data_pd.shape)
    df_1 = hiveCtx.createDataFrame(data_pd)

    table_name = 'da_tmp.test_spark_data'
    df_1.write.saveAsTable(table_name, mode="overwrite")

    # data_d: 类型 pyspark.sql.dataframe.DataFrame
    data_d = hiveCtx.sql("select * from {}".format(table_name))
    print(type(data_d))

    # 存储
    # pandas_df = data_d.toPandas()
    # PandaTool.save(os.path.join(root_path, *["output_path", "tmp_hive_data.xlsx"]), pandas_df)

    # 删除再存储
    # pandas_df['name11'] = "lll"
    # df_2 = hiveCtx.createDataFrame(pandas_df)
    # hiveCtx.sql("drop table if exists {}".format(table_name))
    # df_2.write.saveAsTable(table_name, mode="overwrite")

    # sc.stop()


def drop_hive_tabel(gl_spark):
    hiveCtx = HiveContext(gl_spark.sparkContext)
    hiveCtx.sql("drop table if exists {}".format("da_tmp.my_test"))


if __name__ == '__main__':
    # conf = SparkConf() \
    #     .setAppName("my_first_app_name") \
    #     .setMaster("yarn") \
    #     .set("spark.num-executors", "100")
    #
    # conf.set("spark.executor.memory", "6g")
    # conf.set("spark.executor.cores", "4")
    # conf.set("spark.driver.memory", "1g")
    #
    # # conf.set("spark.dynamicAllocation.maxExecutors", "5")
    # conf.set("spark.shuffle.service.enabled", True)
    # conf.set("spark.dynamicAllocation.enabled", True)
    # conf.set("spark.blacklist.enabled", True)
    #
    # sc = SparkContext(conf=conf)
    # sc.setLogLevel('ERROR')
    # gl_spark = SparkSession(sc)

    gl_spark = SparkSession \
    .builder \
    .appName("my_first_app_name") \
    .getOrCreate()
    sc = gl_spark.sparkContext
    # sqlContext = HiveContext(sc)
    sc.setLogLevel('ERROR')

    test_spark_flow(gl_spark)
    # run_save_hive(gl_spark)
    # drop_hive_tabel(gl_spark)

