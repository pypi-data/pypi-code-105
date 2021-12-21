from distutils.core import setup
from pathlib import Path

import setuptools

setuptools.setup(
    name= "ibraburger",
    version = 1.1,
    long_description= Path("README.rst").read_text(),
    packages = setuptools.find_packages(),
)
