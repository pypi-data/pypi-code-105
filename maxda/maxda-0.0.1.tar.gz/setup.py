# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 
# author : 
# create_time : 2020/7/2 17:21
# update_time : 2020/7/2 17:21
# copyright : Lavector
# ----------------------------------------------
#!/usr/bin/python
# coding:utf-8
from __future__ import print_function
from setuptools import setup, find_packages
import sys
import datetime
import os


version_path = os.path.join(os.getcwd(), *['maxda', "version.py"])
if os.path.exists(version_path):
    version_file = open(version_path)
    cur_version = version_file.readline().strip()
else:
    cur_version = "0.0.1"

setup(
    name="maxda",
    version=cur_version,
    author="lavector data_analysis",
    author_email="guodong.liu@lavector.com",
    description="data process and analysis",
    # license="MIT",
    url="http://gitlab.lavector.com/analysis/maxda-dev.git",
    packages=find_packages(),
    package_data={"maxda": ['maxda/da_all_flow.xml']},
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        # 'Natural Language :: Chinese',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        # 'Topic :: NLP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'pandas>=0.24.2',  # 低版本有一些相关问题，不能使用
        'numpy',
        'xlsxwriter',
        'joblib>=0.14.0',
        'xlrd',
        'pymysql',
        'emoji',
        "sklearn",
        "pyahocorasick",
        "torch>=1.2.0"
    ],
    zip_safe=True,
)
