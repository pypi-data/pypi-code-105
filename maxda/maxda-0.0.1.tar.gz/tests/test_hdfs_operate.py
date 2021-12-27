#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pyhdfs

class HDFSFileManager(object):
    def __init__(self, hosts, user_name):
        self.hosts = hosts
        self.user_name = user_name

    def __get_client(self):
        hf_client = pyhdfs.HdfsClient(hosts=self.hosts, user_name=self.user_name)
        return hf_client

    def upload(self, local_path, hdfs_path):
        print("file upload start")
        hf_client = self.__get_client()
        hf_client.copy_from_local(local_path, hdfs_path)
        print("file upload finish")

    def download(self, hdfs_path, local_path):
        print("file download start")
        hf_client = self.__get_client()
        hf_client.copy_to_local(hdfs_path, local_path)
        print("file download finish")


def main():
    hf = HDFSFileManager(hosts="wacserver2:9870", user_name="hdfs")
    hdfs_path = "/test/测试词表_2.xlsx"
    load_path = "tests/data/test/test_2.xlsx"
    hf.download(hdfs_path, load_path)
    hf.upload(load_path, hdfs_path)


if __name__ == '__main__':
    main()