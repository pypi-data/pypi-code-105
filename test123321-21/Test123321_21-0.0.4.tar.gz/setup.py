#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='Test123321_21', # 项目的名称,pip3 install get-time
    version='0.0.4', # 项目版本 
    author='黄民航', # 项目作者 
    author_email='gmhesat@gmail.com', # 作者email 
    url='https://github.com/nofuck/Data', # 项目代码仓库
    description='获取任意时间/获取当前的时间戳/时间转时间戳/时间戳转时间', # 项目描述 
    packages=['Test123321_21'], # 包名 
    install_requires=[],
    entry_points={
        'console_scripts': [
            
        ]
    } # 重点
)