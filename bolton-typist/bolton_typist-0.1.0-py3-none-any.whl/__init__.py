"""Typing urilities we wish were in the standard library."""

import logging as _logging

from ._core import C, DateLike, E, PathLike, T, assert_never, literal_to_list


__all__ = [
    "C",
    "E",
    "T",
    "DateLike",
    "PathLike",
    "assert_never",
    "literal_to_list",
]

__author__ = "Bryan M Bugyi"
__email__ = "bryanbugyi34@gmail.com"
__version__ = "0.1.0"

_logging.getLogger(__name__).addHandler(_logging.NullHandler())
