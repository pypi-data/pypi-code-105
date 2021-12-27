from collections import ChainMap
from collections.abc import Mapping
from functools import wraps
import string
from typing import Tuple

from ..parsers.parser import build_parser, clean_up_all, build_parsers_map


__ALL__ = ['format']


class SafeFormattingDict(dict):
    # This dictionary allows to keep formatting fields with missing keys unchanged
    def __missing__(self, key):
        return "{{{key}}}".format(key=key)


class CleanUpDict(dict):
    MISSING = ""

    def __missing__(self, key):
        return self.MISSING


class MissingKeysDict(SafeFormattingDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._missing_keys = set()

    def __missing__(self, key):
        self._missing_keys.add(key)
        return "{{{key}}}".format(key=key)

    def missing_keys(self) -> set:
        return self._missing_keys


class SafeFormatter(string.Formatter):
    def check_unused_args(self, used_args, args, kwargs):
        # This function is supposed to raise problems when a key is not used, but was overwritten to do nothing
        pass


def safe_format(s: str, dic: Mapping, missing=True) -> str:
    """
    Default Python formatter that does not raise error if dict has entries that were not used.

    If missing is True,
    entries that were not found in dict are skipped.
    :param s: string to be formatted
    :param dic: formatting entries
    :param missing: if True, missing entries are skipped.
    :return: formatted text
    """
    return SafeFormatter().vformat(s, None, SafeFormattingDict(dic) if missing else dic)


def missing_keys(s: str, dic: Mapping = None) -> set:
    """
    Helper for safe_format that returns keys that were not included in dic. This is useful to prepare a list of
    variables needed for parsing a template string.
    :param s: string to be formatted
    :param dic: map with formatting entries
    :return: set with all entries that were not found in dic.
    """
    dic = MissingKeysDict(dic)
    SafeFormatter().vformat(s, None, dic)
    return dic.missing_keys()


def safe_format_missing(s: str, dic: Mapping) -> Tuple[str, set]:
    """
    This is a combination of safe_format and missing_keys. This is a shortcut that parses that string once with
    variables that were in dic, returning as a result the partially formatted string and a list with missing entries.
    :param s: string to be formatted
    :param dic: map with formatting entries
    :return: tuple with partially formatted string and set with missing entries
    """
    dic = MissingKeysDict(dic)
    result = SafeFormatter().vformat(s, None, dic)
    return result, dic.missing_keys()


def format_element(obj, *args, dic=None, clean_up=False, **kwargs):
    formatted_str = safe_format(obj, dic=dic, missing=False)
    return clean_up_all(formatted_str) if clean_up else formatted_str


def formatter_wrap(parser):

    @wraps(parser)
    def wrapper(obj, dic, defaults=None, missing=True, format_keys=False, **kwargs):
        kwargs.setdefault('parse_keys', format_keys)

        defaults = defaults or dict()

        if missing is True:
            fallback = SafeFormattingDict(defaults)
        elif missing is False:
            fallback = dict(defaults)
        else:
            fallback = CleanUpDict(defaults)
            fallback.MISSING = missing

        formatting_map = ChainMap(dic, fallback)

        return parser(obj, dic=formatting_map, **kwargs)

    return wrapper


STRING_FORMATTERS = build_parsers_map(format_element)


format = formatter_wrap(build_parser(format_element, parsers=STRING_FORMATTERS))
