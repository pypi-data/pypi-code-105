#!/usr/bin/env python3
# *****************************************************************************
# Copyright (C) 2017-2021 Thomas Touhey <thomas@touhey.fr>
# This file is part of the pyfingerd project, which is MIT-licensed.
# *****************************************************************************
""" Defining the native interface. """

from .core import FingerInterface as _FingerInterface

__all__ = ['FingerNativeInterface']


class _FingerNoNativeFoundInterface(_FingerInterface):
    """ Placeholder that doesn't initiate. """

    def __init__(self, *args, **kwargs):
        raise NotImplementedError(
            'Could not find a suitable native interface.',
        )


try:
    from .posix import FingerPOSIXInterface as FingerNativeInterface  # NOQA
except (ImportError, ModuleNotFoundError):
    FingerNativeInterface = _FingerNoNativeFoundInterface

# End of file.
