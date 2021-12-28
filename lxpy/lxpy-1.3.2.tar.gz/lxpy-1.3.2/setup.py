#-*- coding:utf-8 -*-
# @Author  : lx

from distutils.core import setup


with open("README.rst", "r") as f:
  long_description = f.read()

setup(
    name = 'lxpy',
    version = '1.3.2',
    py_modules = ['lxpy'],
    long_description= long_description,
    author = 'ying5338619',
    author_email = '125066648@qq.com',
    url='https://github.com/lixi5338619/lxpy.git',
    #install_requires=["wheel"],
    description = 'Web crawler and data processing toolkit !'
    )
