#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# import findspark
# findspark.init()
import os
import re
import sys
from maxda.analysis.da_tag.tag_deal import TagDealRelationSimple,TagDealSimple
from maxda.analysis.da_tag.mapping_models import MappingCollect, Relation_Mapping_collect
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql import HiveContext
from maxda.analysis.da_tag.tag import TextMatch2, deal_sentence_tag
from maxda.util.panda_tool import PandaTool
import pyhdfs




path_root = os.getcwd()
path_project = os.path.join(path_root, "data")

class FileManager(object):


    def file_upload(self, host, user_name, local_path, hdfs_path):
        print("file upload start")
        fs = pyhdfs.HdfsClient(hosts=host, user_name=user_name)
        # print(fs.listdir('/'))
        fs.copy_from_local(local_path, hdfs_path)
        print("file upload finish")


    def file_down(self, host, user_name, local_path, hdfs_path):
        print("file download start")

        fs = pyhdfs.HdfsClient(hosts=host, user_name=user_name)
        fs.copy_to_local(hdfs_path, local_path)
        print("file download finish")

class TagDealRelationSimpleHan(object):
    def __init__(self):
        pass

    def process(self, data, tag_config_path):
        data = data.asDict()
        # tag_config_path = os.path.join(path_project, "data/relation_tag.xlsx")

        mapping = Relation_Mapping_collect(tag_config_path)
        data['rag_results'] = str(deal_sentence_tag(data,mapping))
        return data


def main():
    spark = SparkSession \
        .builder \
        .appName('my_first_app_name') \
        .getOrCreate()
    sc = spark.sparkContext
    sc.setLogLevel('ERROR')

    hiveCtx = HiveContext(sc)

    #从hdfs获取配置文件到本地路径/data/var/da， 然后从本地读取。
    file_manager = FileManager()
    host = "wacserver2:9870"
    user_name = "hdfs"
    local_path = "/data/var/da/relation_tag.xlsx"
    hdfs_path = "/test/relation_tag.xlsx"
    file_manager.file_down(host,user_name,local_path,hdfs_path)

    #打标
    tag_friend = TagDealRelationSimpleHan()

    # tag_config_path = os.path.join(path_project, "data/test_spark_data.xlsx")
    # color_df = PandaTool.read(tag_config_path)
    # data_d = spark.createDataFrame(color_df)

    #从hive中获取数据
    data_d = hiveCtx.sql("select * from test.test_spark_data")

    color_df = data_d.rdd.map(lambda r: tag_friend.process(r, local_path))

    test_q = color_df.collect()
    data_all = spark.createDataFrame(test_q)
    data_all.show()



if __name__ == '__main__':
    main()