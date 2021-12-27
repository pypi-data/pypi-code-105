# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages
from qrunner import __version__, __description__

try:
    long_description = open(os.path.join('qrunner', "README.md"), encoding='utf-8').read()
except IOError:
    long_description = ""

setup(
    name="qrunner",
    version=__version__,
    description=__description__,
    author="杨康",
    author_email="772840356@qq.com",
    url="https://github.com/bluepang/qrunner",
    platforms="Android,IOS,Web",
    packages=find_packages(),
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
    ],
    include_package_data=True,
    package_data={
        r'': ['*.exe'],
    },
    install_requires=['tidevice', 'facebook-wda', 'uiautomator2', 'selenium', 'pytest', 'pytest-html',
                      'pytest-rerunfailures', 'allure-pytest', 'pytest-dependency==0.5.1', 'pandas==1.3.4',
					  'openpyxl==3.0.9', 'XlsxWriter==3.0.2'],
    entry_points={
        'console_scripts': [
            'qrun = qrunner.cli:main',
            'qrunner = qrunner.cli:main'
        ]
    },
)
