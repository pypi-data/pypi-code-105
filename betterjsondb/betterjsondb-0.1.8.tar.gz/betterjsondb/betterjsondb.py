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

from .exceptions import raiseWarning


def get_standards_read(filename: str) -> str:
    """Return standard code for exec().reading."""
    return f"""import json\n\nwith open("{filename}", "r") as dbfile:\n    data = json.load(dbfile)\n\n"""


def get_standard_write(filename: str) -> str:
    """Return standard code for exec().writing."""
    return f"""\n\nwith open("{filename}", "w") as dbfile:\n    json.dump(data, dbfile)\n\n"""


def splitter(key: str, prefix: str) -> str:
    """Split key by its prefix."""
    key = key.split(prefix)
    if isinstance(key, list):
        tojsonpath = "".join(f"['{i}']" for i in key)
    else:
        tojsonpath = f"['{key}']"

    return tojsonpath


class connect:
    """Class that being container for working with files."""
    def __init__(self, file: str, prefix: str) -> typing.NoReturn:
        self.file = file
        self.prefix = prefix
        try:
            with open(self.file, "r"):
                pass
        except FileNotFoundError:
            with open(self.file, "x") as file:
                file.write("{}")
            raiseWarning(self.file, "FileNotFoundError")

    def get(self, key: str) -> typing.Any:
        """Search and return key from file if exists, else you'll get error."""
        result = {}
        if key == "all":
            exec(f"{get_standards_read(self.file)}"
                 f"final_result = data", result)
            return result["final_result"]
        else:
            exec(f"{get_standards_read(self.file)}"
                 f"final_result = data{splitter(key, self.prefix)}", result)
            return result["final_result"]

    def push(self,
             key: str,
             value: typing.Any,
             callback: bool = False) -> typing.Union[bool, None]:
        """Write information to file if key's NOT exists.
        So function, create key and after update data here."""
        if isinstance(value, str):
            value = f"'{value}'"

        exec(f"{get_standards_read(self.file)}"
             f"data{splitter(key, self.prefix)}={value.__class__.__name__}({value})"
             f"{get_standard_write(self.file)}")
        if callback is True:
            return True

    def update(self,
               key: str,
               operator: str,
               value: typing.Any,
               callback: bool = False) -> typing.Union[bool, None]:
        """Write information to file if key's EXISTS."""
        if isinstance(value, str):
            value = f"'{value}'"

        exec(f"{get_standards_read(self.file)}"
             f"data{splitter(key, self.prefix)}{operator}{value.__class__.__name__}({value})"
             f"{get_standard_write(self.file)}")
        if callback is True:
            return True

    def delete(self,
               key: str,
               callback: bool = False) -> typing.Union[bool, None]:
        """Delete information from file."""
        exec(f"{get_standards_read(self.file)}"
             f"del data{splitter(key, self.prefix)}"
             f"{get_standard_write(self.file)}")
        if callback is True:
            return True
