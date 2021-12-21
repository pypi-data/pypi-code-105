# -*- coding: utf-8 -*-
import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="aigofirst",
    version="0.0.1",
    author="lycra",
    author_email="lycrali@careerintlinc.com",
    description="初始化",
    long_description=long_description,
    url="https://git.geedos.com/algorithm/aigo",
    packages=setuptools.find_packages(),

    python_requires='>=3.6',
)
