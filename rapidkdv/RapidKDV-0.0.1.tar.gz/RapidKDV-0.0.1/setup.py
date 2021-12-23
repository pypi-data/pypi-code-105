#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Kerple GL Plugin
# Mail: 123456@qq.com
# Created Time:  2021-12-22 19:17:34
#############################################

from setuptools import setup, find_packages   

setup(
    name = "RapidKDV",
    version = "0.0.1",
    keywords = ["pip", "KDV","heatmap"],
    description = "KDV",
    long_description = "An feature heatmap algorithm",
    license = "MIT Licence",

    url = "https://github.com/libkdv",  
    author = "Kerple GL Plugin",
    author_email = "123456@qq.com",

    packages = find_packages('rapidkdv'),
    include_package_data = True,
    platforms = "any",
    install_requires = ["numpy","pydeck"]        
)