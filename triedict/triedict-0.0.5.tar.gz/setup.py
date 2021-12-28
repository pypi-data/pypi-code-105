# -*- coding: UTF-8 -*-
"""vega FYI
    @author: vegaviazhang
    @file:setup.py
    @time:2021/10/04
"""
from setuptools import setup, find_packages

setup(
    name='triedict',
    version="0.0.5",
    description=(
        '基于字典树的匹配 请移步github官网查看demo https://github.com/vegaviazhang/triedict'
    ),
    # long_description=open('README.rst').read(),  # 不会这个语法，hhh
    author='vegaviazhang',
    author_email='vegaviazhang@gmail.com',
    maintainer='vega',
    maintainer_email='vegaviazhang@gmail.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/vegaviazhang/triedict',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[]
)
