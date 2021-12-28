#!/usr/bin/env python

import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setuptools.setup(
    name='PyTaskFarmer',
    version='0.0.1',
    description='Simple task farmer using file locks to syncrhonize among multiple nodes.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://gitlab.cern.ch/berkeleylab/pytaskfarmer',
    packages=['taskfarmer'],
    scripts=['pytaskfarmer.py']
    )
