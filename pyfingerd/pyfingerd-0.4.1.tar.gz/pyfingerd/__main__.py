#!/usr/bin/env python3
# *****************************************************************************
# Copyright (C) 2017-2021 Thomas Touhey <thomas@touhey.fr>
# This file is part of the pyfingerd project, which is MIT-licensed.
# *****************************************************************************
""" Main script of the module. """

from .cli import cli as _cli

__all__ = []

if __name__ == '__main__':
    _cli()

# End of file.
