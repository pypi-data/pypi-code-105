import pathlib
import setuptools
from setuptools import setup

HERE=pathlib.Path(__file__).parent

setup(
    name ="flame_para_l",
    version = "1.0.0",
    author = "Urmila",
    author_email = "urmilaraj18@gmail.com",
    description = "testing_packages",
    long_description ="long_description",
    long_description_content_type = "text/markdown",
    license="MIT",
    classifiers = [
       "License :: OSI Approved :: MIT License",
       "Programming Language :: Python :: 3.6",
       "Programming Language :: Python :: 3.7",
       "Programming Language :: Python :: 3.8",
    ],
    packages=["para"],
    install_requires=[],
    include_package_data=True,
)


