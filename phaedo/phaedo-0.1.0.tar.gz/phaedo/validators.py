import re
from .core.validation import Validator


def mandatory():
    return Validator(lambda v: v is not None, 'cannot be None')


def max_length(length: int):
    return Validator(lambda v: v is None or len(v) <= length, f'The length of value must be less than {length}')


def min_length(length: int):
    return Validator(lambda v: v is None or len(v) >= length, f'The length of value must be more than {length}')


def regex(pattern: str):
    return Validator(lambda v: v is None or re.match(pattern, v), 'invalid value')


def url():
    return regex(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+')


def mailaddress():
    return regex(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')


def value_in(values: list):
    return Validator(lambda v: v is None or v in values, 'invalid value')
