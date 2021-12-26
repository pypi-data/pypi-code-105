import os

from setuptools import setup, find_packages

setup(
    name="pkgparser",
    description="Python package for parsing metadata from classes and functions in a python package.",
    long_description=open(os.path.join(os.getcwd(), "README.md")).read().strip(),
    version=open(os.path.join(os.getcwd(), "VERSION")).read().strip(),
    url="https://gitlab.com/lgensinger/pkgparser",
    install_requires=[d.strip() for d in open(os.path.join(os.getcwd(), "requirements.txt")).readlines()],
    extras_require={
        "test": [d.strip() for d in open(os.path.join(os.getcwd(), "requirements-test.txt")).readlines()] if os.path.exists(os.path.join(os.getcwd(), "requirements-test.txt")) else list()
    },
    packages=find_packages(),
    include_package_data=True
)
