# #!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/12/16 16:55
# @Author : BruceLong
# @FileName: config.py
# @Email   : 18656170559@163.com
# @Software: PyCharm
# @Blog ：http://www.cnblogs.com/yunlongaimeng/


# ***************Kafka配置-start*********************
KAFKA_HOST = '127.0.0.1'
KAFKA_PORT = '6667'
KAFKA_TOPIC_NEW = 'colourdata_bbs'
KAFKA_TOPIC_BACK = 'VIDEO_BBS'
KAFKA_PARTITION = 4
KAFKA_TOPIC_TEST = 'test_addFile'
# ***************Kafka配置-end*********************


# ***************mongo数据库配置-start*********************
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "ClientIds"
# ***************mongo数据库配置-end*********************

# ***************SqlServer数据库配置-start*********************
SQLSERVER_HOST = '127.0.0.1'
SQLSERVER_USERNAME = 'brucelong'
SQLSERVER_PASSWORD = 'adminroot'
SQLSERVER_DB = 'CDDST'
# ***************SqlServer数据库配置-end*********************


# ***************MySQL数据库配置-start*********************
# MYSQL_HOST = '192.168.0.112'
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = '3306'
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_DB = 'cddst'
# ***************MySQL数据库配置-end*********************
