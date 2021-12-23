# -*- coding: utf-8 -*-
# @File    :   setup.py
# @Time    :   2021/12/23 17:11:17
# @Author  :   Cen Jinglun
# @Contact :   cenjinglun@qq.com

from setuptools import setup, find_packages  #这个包没有的可以pip一下

setup(
    name="CJLTools",  #这里是pip项目发布的名称
    version="0.0.3",  #版本号，数值大的会优先被pip
    keywords=("pip", "CJLTools", "Small Tools"),
    description="Some small tools",
    long_description="Some small tools",
    license="MIT Licence",
    url="https://github.com/cenjinglun/CJLTools",  #项目相关文件地址，一般是github
    author="Jinglun Cen",
    author_email="cenjinglun@qq.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["pyyaml", "Pillow"]  #这个项目需要的第三方库
)

# 运行命令
# python setup.py sdist
# 上传
# twine upload dist/xxx.tar.gz
