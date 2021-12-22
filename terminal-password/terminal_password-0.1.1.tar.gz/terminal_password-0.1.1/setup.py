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
    version="0.1.1",
    keywords=["password","terminal"],
    description="a tool for input cipher password",
    long_description=read_file('README.rst'),
    platforms="any",
    data_files=["img/terminal_password.gif"],
    packages = find_packages(),
    ext_modules=[module],
    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.4"
)