#!/usr/bin/env python
# coding: utf-8
"""Utils module"""


__all__ = [
    'json_encode',
    'is_private',
    'unprivate',
    'remove_accents',
    'today',
    'normalize',
    'age',
    'today',
    'now',
    'is_defined',
    'is_missing',
    'exist',
    'only_digits',
    'no_digits',
    'split_digits_and_letters',
    'zip_longest',
    'semicolon_split',
    'comma_split',
    'list_phrases',
    'process_branded_drug',
    'cammel_case',
    'list_words',
    'group_words',
    'check'
    ]

import re
import itertools
from enum import Enum 
from dataclasses import MISSING
from datetime import timedelta, date, datetime
from decimal import Decimal
import unicodedata 
from typing import Union

today = date.today
now = datetime.now
normalize = lambda string: unicodedata.normalize('NFKD', string)

def age(birthdate: Union[date, str]) -> int:
    return ((today() - birthdate if isinstance(birthdate, date) else date.fromisoformat(birthdate)).days/365).__round__(2)

def remove_accents(string: str) -> str:
    return ''.join([c for c in normalize(string) if not unicodedata.combining(c)])

def is_private(string: str) -> bool:
    return True if string.startswith("_") and not string.endswith("_") else False

def unprivate(string: str) -> str:
    return string[ 1: ] if is_private(string) else string

def json_encode(value):
    if value == None:
        return ''
    elif isinstance(value, bool):
        return value
    elif isinstance(value, (str, int, float)):
        return value
    elif isinstance(value, Decimal):
        return str(value)
    elif isinstance(value, list):
        return [json_encode(i) for i in value]
    elif isinstance(value, dict):
        return {unprivate(k): json_encode(v) for k, v in value.items()}
    elif isinstance(value, Enum):
        return str(value)
    elif isinstance(value, (datetime, date)):
        return value.isoformat()
    elif isinstance(value, timedelta):
        return f'{value.days} {"dias"  if value.days > 1 else "dia"}'
    elif isinstance(value, tuple):
        try:
            return {k: json_encode(v) for (k,v) in value._asdict().items()}
        except:
            return [json_encode(v) for v in value]
    else:
        return str(value)

def is_defined(value):
    return False if value == '<undefined>' else True

def is_missing(value):
    return True if value == '<missing>' else False

def exist(value):
    return False if value in ['', None, '<missing>', '<undefined>'] else True

def semicolon_split(string: str):
    return [x.strip() for x in string.split(';')]

def comma_split(string: str):
    return [x.strip() for x in string.split(',')]

def list_phrases(string: str):
    norm = lambda x: x[0].upper() + x[1:] + '.'
    data = [x.strip() for x in re.split(r'\.\s', string) if exist(x)]
    return [norm(x) for x in data]

def only_digits(value):
    return ''.join(filter(lambda x: x.isdigit() or x in ['.'], value))

def no_digits(value):
    return ''.join(filter(lambda x: True if not x.isdigit() and not x in ['.'] else False, value))

def split_digits_and_letters(value):
    '''Returns a tuple with numbers as index 0 and letters as index 1'''
    return eval(only_digits(value)) if only_digits(value) else None, no_digits(value)


def zip_longest(*args):
    return itertools.zip_longest(*args)

def process_branded_drug(brand: dict):
    presentations = semicolon_split(brand['sets'])
    strengths, quantities = [], []
    for item in presentations:
        data = [x.strip() for x in item.split()]
        strengths.append(data[:-1])
        quantities.append(data[-1])
    return [[semicolon_split(brand['drugs']), *x, brand['recipe'], brand['name'], brand['pharmaceutical']] for x in zip_longest(strengths, quantities)]

def cammel_case(string: str):
    return ''.join([x.strip() for x in remove_accents(string).split()])


def list_words(string: str):
    return [x.strip() for x in string.split(' ')]



def group_words(text: str):
    p = re.compile(r'(?P<word>\b\w+\b)')
    return p.findall(text)


def check(function, iterable):
    gen = (x for x in iterable)
    result = []
    try:
        while True:
            result.append(function(next(gen)))
    except StopIteration:
        pass 
    finally:
        return any(result)