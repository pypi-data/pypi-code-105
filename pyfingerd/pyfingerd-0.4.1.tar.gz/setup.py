#!/usr/bin/env python3
# *****************************************************************************
# Copyright (C) 2018-2021 Thomas Touhey <thomas@touhey.fr>
# This file is part of the pyfingerd project, which is MIT-licensed.
# *****************************************************************************
""" Setup script for the pyfingerd Python package. """

import os.path as _path
from setuptools import setup as _setup

kwargs = {}

# Add requirements using the requirements.txt file.

requirements = set()
with open(_path.join(_path.dirname(__file__), 'requirements.txt'), 'r') as f:
    requirements.update(f.read().splitlines())

kwargs['install_requires'] = sorted(filter(lambda x: x, requirements))

# Use Sphinx for building docs.

try:
    from sphinx.setup_command import BuildDoc as _BuildDoc
    kwargs['cmdclass'] = {'build_sphinx': _BuildDoc}
except ImportError:
    pass

# Actually, most of the project's data is read from the `setup.cfg` file.

kwargs['setup_requires'] = ['flake8']

_setup(
    **kwargs,
)

# End of file.
