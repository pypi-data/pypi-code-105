# coding=utf-8
#
# This file is part of hARPy
# See https://github.com/serhatcelik/harpy for more information
# Released under the MIT license
# Copyright (C) Serhat Çelik

"""hARPy -who uses ARP- - Active/passive ARP discovery tool."""

from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import threading

_OS = ("posix",)

if sys.version_info[0] == 2:
    _MIN_PY = (2, 7)
else:
    _MIN_PY = (3, 4)

###############
# Requirement #
###############
_REQ_OS = _OS

_REQ_PY_MAJOR = _MIN_PY[0]
_REQ_PY_MINOR = _MIN_PY[1]
_REQ_PY = "%d.%d+" % (_REQ_PY_MAJOR, _REQ_PY_MINOR)

###########
# Current #
###########
_NOW_OS = os.name

_NOW_PY_MAJOR = sys.version_info[0]
_NOW_PY_MINOR = sys.version_info[1]
_NOW_PY = "%d.%d" % (_NOW_PY_MAJOR, _NOW_PY_MINOR)

if _NOW_PY_MAJOR != _REQ_PY_MAJOR or _NOW_PY_MINOR < _REQ_PY_MINOR:
    print("[!] Expected Python %s, got Python %s instead" % (_REQ_PY, _NOW_PY))
    sys.exit(2)
if _NOW_OS not in _REQ_OS:
    print("[!] Unsupported operating system for hARPy:", _NOW_OS)
    sys.exit(2)


# Workaround for sys.excepthook thread bug
def install_thread_excepthook():
    """See https://bugs.python.org/issue1230540 for details."""
    init_original = threading.Thread.__init__

    def init(self, *args, **kwargs):
        """Docstring."""
        init_original(self, *args, **kwargs)
        run_original = self.run

        def run(*args2, **kwargs2):
            """Docstring."""
            try:
                run_original(*args2, **kwargs2)
            except Exception:  # pylint: disable=broad-except
                sys.excepthook(*sys.exc_info())

        self.run = run

    threading.Thread.__init__ = init


install_thread_excepthook()
