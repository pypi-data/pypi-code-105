#!/usr/bin/env python

from io import open
from setuptools import setup

"""
:authors: Runner
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2021 Peopl3s
"""

version = '1.0.1'

long_description = ""

setup(
    name='hw_bonus_point_api',
    version=version,

    author='Runner',
    author_email='levintsov.v.v@gmail.com',

    description=(
        u'Python module for writing scripts for project management platform '
        u'Club House (clubhouse.io API wrapper)'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/EgorMozharov/hw_bonus_point',
    download_url='https://github.com/EgorMozharov/hw_bonus_point/archive/v{}.zip'.format(version),

    license='Apache License, Version 2.0, see LICENSE file',

    packages=['hw_bonus_point_api'],
    install_requires=['aiohttp', 'aiofiles'],

    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
