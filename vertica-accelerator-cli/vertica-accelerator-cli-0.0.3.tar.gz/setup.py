#!/usr/binf/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Created on September 29 10:32 2021
# (c) Copyright 2021 Micro Focus or one of its affiliates.
# ------------------------------------------------------------------------------
from setuptools import setup
from shutil import rmtree
from setuptools import find_packages, setup, Command
import io
import os
import sys

# Package meta-data
VCLI_NAME = 'vertica-accelerator-cli'
VCLI_DESC = 'Vertica Command Line Interface'
VCLI_URLS = 'https://github.com/vertica/vertica-accelerator-cli'
VCLI_EMAIL = 'xj.he@microfocus.com, hao.yang@microfocus.com, kirtan.chavda@microfocus.com'
VCLI_AUTHOR = 'XJ, Hao Yang, Kirtan Chavda'
VCLI_REQUIRES_PYTHON = '>=3.7'
VCLI_VERSION = '0.0.3'

# Required packages for VCLI to be executed
VCLI_REQUIRED_PACKAGES = [
    'setuptools_rust==0.12.1',
    'pkce==1.0.3',
    'requests==2.24.0',
    'environs==9.3.4',
    'argcomplete==1.12.3',
    'python-dateutil==2.8.2',
    'six==1.16.0',
    'pytest==6.2.5'
]

# Optional packages
VCLI_EXTRAS_PACKAGES = {

}

current_folder = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as long-description.
try:
    with io.open(os.path.join(current_folder, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = VCLI_DESC

# Load the package's __version__.py module as a dictionary
about = {}
if not VCLI_VERSION:
    project_slug = VCLI_NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(current_folder, project_slug, '__version__.py'), encoding='utf-8') as f:
        exec(f.read(), about)
else:
    about['__version__'] = VCLI_VERSION

setup(
    name=VCLI_NAME,
    version=about['__version__'],
    packages=find_packages(exclude=['ez_setup', 'tests', '*.tests', '*.tests.*', 'tests.*']),
    url=VCLI_URLS,
    license='(c) Copyright 2021 Micro Focus or one of its affiliates.',
    author=VCLI_AUTHOR,
    author_email=VCLI_EMAIL,
    description=VCLI_DESC,
    python_requires=VCLI_REQUIRES_PYTHON,
    package_data={'': ['logging.conf']},
    entry_points={
        'console_scripts': [
            'va=vcli.vcli_main:va_command'
        ]
    },
    install_requires=VCLI_REQUIRED_PACKAGES,
    extras_require=VCLI_EXTRAS_PACKAGES,
    include_package_date=True,
    classifiers=[
        # VCLI classifiers
        # Full list: https://pypi.pthon.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],

    # Todo: publish support
    cmdclass={

    }
)
