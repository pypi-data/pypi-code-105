from setuptools import setup

with open("README.md","r") as fh:
    long_description=fh.read()

setup(
name='PyMyOracle',
version='0.0.1',
description='Simple Oracle API to view data in Python dataframe',
long_description=long_description,
long_description_content_type="text/markdown",
py_modules=["PyMyOracle"],
pacakage_dir={'':'src'},
install_requires = [
        'cx_Oracle',
        'pandas'
    ]
)
