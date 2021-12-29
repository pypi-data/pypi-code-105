# #!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/12/29 11:20
# @Author : BruceLong
# @FileName: setup.py
# @Email   : 18656170559@163.com
# @Software: PyCharm
# @Blog ：http://www.cnblogs.com/yunlongaimeng/
from setuptools import setup, find_packages

setup(
    name="cddst",
    version="0.0.4",
    packages=find_packages(),
    author="BruceLong",
    license="MIT Licence",
    author_email="18656170559@163.com",
    include_package_data=True,
    platforms="any",
    install_requires=['PyMySQL>=1.0.2']
)
