# -*- coding: utf-8 -*-

import setuptools
from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="draftapp",
    version="0.1.4",
    author="Ratan Boddu",
    author_email="ratanboddu@gmail.com",
    description="Build scalable production-grade web applications within seconds",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ratanboddu/draftapp",
    project_urls={
        "Bug Tracker": "https://github.com/ratanboddu/draftapp/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    install_requires=[
        "click==8.0.3"
    ],
    python_requires=">=3.6",
    scripts=["bin/draftapp"],
    packages=['draftapp'],
    include_package_data=True,
)
