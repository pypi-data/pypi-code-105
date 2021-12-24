#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import setuptools

with open("README.md", 'r', encoding='utf-8') as f:
    long_description = f.read()

with open("requirements.txt", 'r', encoding='utf-8') as f:
    requirements = f.read().split()

setuptools.setup(
    name="air-df",  # pip install name
    version="0.0.7",
    author="Damon",
    author_email="527439841@qq.com",
    description="常用插件",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Air-df",  # 项目地址
    packages=['air'],
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=[
        'air.base_handler', 'air.plugins'
    ]
)
