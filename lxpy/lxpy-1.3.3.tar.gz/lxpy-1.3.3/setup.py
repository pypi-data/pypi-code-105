#-*- coding:utf-8 -*-
# @Author  : lx

#from distutils.core import setup
from setuptools import setup, find_packages



with open("README.rst", "r") as f:
  long_description = f.read()

setup(
    name = 'lxpy',
    version = '1.3.3',
    #py_modules = ['lxpy'],
    long_description= long_description,
    packages=find_packages(),
    author = 'ying5338619',
    license= 'MIT License',
    author_email = '125066648@qq.com',
    url='https://github.com/lixi5338619/lxpy.git',
    install_requires=["wheel"],
    description = 'Web crawler and data processing toolkit !'
    )

# python setup.py sdist build
# python setup.py sdist bdist_wheel
# twine upload dist/*
