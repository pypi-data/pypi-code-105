#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from setuptools import setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    path = os.path.join(package, "__init__.py")
    init_py = open(path, "r", encoding="utf8").read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_long_description():
    """
    Return the README.
    """
    return open("README.md", "r", encoding="utf8").read()


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


env_marker_cpython = (
    "sys_platform != 'win32'"
    " and (sys_platform != 'cygwin'"
    " and platform_python_implementation != 'PyPy')"
)

env_marker_win = "sys_platform == 'win32'"

minimal_requirements = [
    "asgiref>=3.4.0",
    "click>=7.0",
    "h11>=0.8",
]


extra_requirements = [
    "websockets>=10.0",
    "httptools>=0.2.0,<0.4.0",
    "uvloop>=0.14.0,!=0.15.0,!=0.15.1; " + env_marker_cpython,
    "colorama>=0.4;" + env_marker_win,
    "watchgod>=0.6",
    "python-dotenv>=0.13",
    "PyYAML>=5.1",
]


setup(
    name="esg",
    version=get_version("esg"),
    url="https://github.com/mtag-dev/esg",
    license="BSD",
    description="Enhanced Service Gateway",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Stanislav Dubrovskyi",
    author_email="s.dubrovskyi@cleverdec.com",
    packages=get_packages("esg"),
    install_requires=minimal_requirements,
    extras_require={"standard": extra_requirements},
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    entry_points="""
    [console_scripts]
    esg=esg.main:main
    """,
    project_urls={
        "Source": "https://github.com/mtag-dev/esg",
        "Changelog": "https://github.com/mtag-dev/esg/blob/master/CHANGELOG.md",
    },
)
