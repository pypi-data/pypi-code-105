#!/usr/bin/env python3

'''
setuptools-based setup module; see:

-   https://packaging.python.org/guides/distributing-packages-using-setuptools/
-   https://github.com/pypa/sampleproject
'''

from setuptools import find_packages
from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='logging-ext',
    version='1.0.2',
    packages=find_packages(),
    url='https://github.com/cykerway/logging-ext',
    author='Cyker Way',
    author_email='cykerway@example.com',
    description='logging extension;',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development',
    ],
    keywords='logging,extension',
    package_data={
    },
    data_files=[
    ],
    install_requires=[
    ],
    extras_require={
    },
    entry_points={
    },
    project_urls={
        'Funding': 'https://paypal.me/cykerway',
        'Source':  'https://github.com/cykerway/logging-ext/',
        'Tracker': 'https://github.com/cykerway/logging-ext/issues',
    },
)

