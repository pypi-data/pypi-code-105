#!/usr/bin/env python3

from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='kiddeemata',
    packages=['kiddeemata'],
    install_requires=['pyserial', 'Pillow', 'pygame'],

    version='1.4.1',
    description="A Python Protocol Abstraction Library For Arduino Firmata - Updated by Kiddee Lab",
    long_description=long_description,
    long_description_content_type='text/markdown',

    author='Kiddee Lab',
    author_email='kiddeelab2@gmail.com',
    url='https://github.com/xavjb/kiddeemata',
    download_url='https://github.com/xavjb/kiddeemata',
    keywords=['Firmata', 'Arduino', 'Protocol', 'Python', 'Kiddee Lab'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)