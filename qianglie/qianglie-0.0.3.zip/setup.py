#!/usr/bin/env python
# coding: utf-8
import os
from setuptools import setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name='qianglie',
    version='0.0.3',
    author='qianglie',
    author_email='qianglie@me.com',
    url='https://www.qianglie.com',
    description='qianglie',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    license='MIT',
    packages=['qianglie'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    project_urls={
        'Telegram': 'https://t.me/qianglie',
        'Twitter': 'https://twitter.com/qianglie',
        'Source': 'https://github.com/qianglie/domain',
        'Documentation': 'https://www.qianglie.com/knowledgebase'
    },
)
