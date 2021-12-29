#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
File Name: setup.py
Author: gadfy
"""

from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "samebirthdayrate",      #这里是pip项目发布的名称
    version = "1.0.0",  #版本号，数值大的会优先被pip
    keywords = ("pip","samebirthdayrate"),
    description = "caculate same birthday rate",
    long_description = "x pepole, caculate the percentage of birth in same date at least two",
    license = "MIT Licence",

    url = "https://narwelplists.herokuapp.com/",     #项目相关文件地址，一般是github
    author = "gadfy",
    author_email = "gadfy_m@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []          #这个项目需要的第三方库
)
