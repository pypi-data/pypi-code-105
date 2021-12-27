# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2021 Dallas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import typing
import sys
import os

from .static.color_dict import textColor


class raiseWarning:
    """Small exceptions, that not being problem for correct job."""
    def __init__(self, _executed_file: str, _warn_type: str) -> typing.NoReturn:
        """Raise warnings to make user know if something happend."""
        system_split = "{}".format("\\" if sys.platform == "win32" else "/")
        print(
            "\n" + self._warn_matcher(_warn_type).format(
                os.getcwd() + system_split + _executed_file
            ),
            end="\n\n"
        )

    @staticmethod
    def _warn_matcher(_warn_type: str) -> str:
        """Searching matching warnings and its description."""
        match _warn_type:
            case "FileNotFoundError":
                return textColor.yellow + "Warning: Don't found such file: {}.\nCreated new." + textColor.reset
            case base:
                return textColor.yellow + "Warning: Unknown warning: {}." + textColor.reset
