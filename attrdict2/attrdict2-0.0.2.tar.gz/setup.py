"""
To install AttrDict:

    python setup.py install
"""
from setuptools import setup


setup(
    author       = "ofarukbicer",
    author_email = "omerfarukbicer0446@gmail.com",

    packages     = ["attrdict2"],

    name         = "attrdict2",
    version      = "0.0.2",
    url          = "https://github.com/ofarukbicer/AttrDict",
    description  = "Siz uğraşmayın diye biz uğraştık.. ~ dızz 🐍",
    keywords     = ["AttrDict", "KekikAkademi", "ofarukbicer", "keyiflerolsun"],

    long_description_content_type   = "text/markdown",
    long_description                = "".join(open("README.md", encoding="utf-8").readlines()),
    include_package_data            = True,

    license      = "MIT License",

    classifiers  = (
        "Development Status :: 7 - Inactive",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ),
    install_requires = (
        'six',
    ),
    tests_require    = (
        'nose>=1.0',
        'coverage',
    ),
)