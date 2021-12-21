#encoding:utf-8
import os
from setuptools import setup, Extension
from setuptools import setup, find_packages

def read_file(filename):
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            filename)
    if os.path.exists(filepath):
        return open(filepath,encoding="utf-8").read()
    else:
        return ''

module = Extension("terminal_password", sources=["password.c"])
setup(
    name="terminal_password",
    version="0.1",
    keywords=('password','terminal'),
    description="a tool for input cipher password",
    long_description=read_file('README.rst'),
    platforms="any",
    packages = find_packages(),
    ext_modules=[module]
)