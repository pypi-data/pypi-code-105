"""I/O ninja (ION)... Utilities related to I/O that we find useful."""

import logging as _logging

from ._core import confirm, copy_to_clipboard, efill, ewrap, getch


__all__ = ["confirm", "copy_to_clipboard", "efill", "ewrap", "getch"]

__author__ = "Bryan M Bugyi"
__email__ = "bryanbugyi34@gmail.com"
__version__ = "0.1.0"

_logging.getLogger(__name__).addHandler(_logging.NullHandler())
