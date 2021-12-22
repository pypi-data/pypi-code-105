from distutils.core import setup

setup(
    name = "baizhanMathLZY123",#对外模块的名字
    version = "1.0",#版本号
    description = "只是第一个对外发布的模块，测试",#描述
    author = "吕泽宇",#作者
    author_email= "653187469@qq.com",#作者邮箱
    py_modules = ["baizhanMath.demo_1","baizhanMath.demo_2"]#需要发布的模块
)