#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="sentry-notice",
    version='1.0.4',
    author='spxinjie6',
    author_email='1311855817@qq.com',
    url='https://github.com/spxinjie6/sentry-notice.git',
    description='sentry 接入dingTalk 告警',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    keywords='python sentry dingTalk notice',
    include_package_data=True,
    zip_safe=False,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'requests',
    ],
    entry_points={
        'sentry.plugins': [
            'sentry_notice = sentry_notice.plugin:DingTalkPlugin'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
    ]
)
