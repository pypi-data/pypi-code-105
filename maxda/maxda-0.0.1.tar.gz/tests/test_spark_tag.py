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
from pyspark.sql.types import *
from pyspark.sql import HiveContext
from maxda.analysis.da_tag.tag import TextMatch2, deal_sentence_tag
from maxda.util.panda_tool import PandaTool


# global path_root, path_project
path_root = os.getcwd()
path_project = os.path.join(path_root, "data")
input_data_path = os.path.join(path_project, "1_log")
output_data_path2 = os.path.join(path_project, "3_clean/微博用户1.xlsx")


class TagDealRelationSimpleHan(object):
    def __init__(self):
        pass

    def process(self, data):
        data = data.asDict()
        # tag_config_path = os.path.join("C:/Users/zhang/han/maxda-dev/dataset/config_path/relation_tag.xlsx")
        tag_config_path = os.path.join(path_project, "relation_tag.xlsx")
        mapping = Relation_Mapping_collect(tag_config_path)
        data['rag_results'] = str(deal_sentence_tag(data,mapping))
        return data

def main():

    spark = SparkSession \
        .builder \
        .appName('my_first_app_name') \
        .getOrCreate()
    sc = spark.sparkContext
    # sqlContext = HiveContext(sc)
    sc.setLogLevel('ERROR')
    StringType
    tag_fridend = TagDealRelationSimpleHan()
    # color_df = PandaTool.read("C:/Users/zhang/han/maxda-dev/dataset/config_path/test_spark_data.xlsx")
    # my_dataframe = sqlContext.sql("Select * from test.write_table limit 10")
    tag_config_path = os.path.join(path_project, "test_spark_data.xlsx")
    color_df = PandaTool.read(tag_config_path)
    data_d = spark.createDataFrame(color_df)
    color_df_result = data_d.rdd.map(lambda r: tag_fridend.process(r))
    #
    test_q = color_df_result.collect()
    data_all = spark.createDataFrame(test_q)
    data_all.show()


if __name__ == '__main__':
    main()