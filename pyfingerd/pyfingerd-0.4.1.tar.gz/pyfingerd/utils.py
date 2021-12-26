#!/usr/bin/env python3
# *****************************************************************************
# Copyright (C) 2021 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the pyfingerd Python 3.x module, which is MIT-licensed.
# *****************************************************************************
""" Utilities for the pyfingerd module. """

import logging as _logging
import re as _re

from datetime import timedelta as _td
from typing import Optional as _Optional, Union as _Union

__all__ = [
    'access_logger', 'error_logger', 'format_delta', 'logger', 'parse_delta',
]

__delta0_re = _re.compile(r'(-?)(([0-9]+[a-z]+)+)')
__delta1_re = _re.compile(r'([0-9]+)([a-z]+)')

logger = _logging.getLogger('pyfingerd')
access_logger = _logging.getLogger('pyfingerd.access')
error_logger = _logging.getLogger('pyfingerd.error')


def parse_delta(raw: str) -> _td:
    """ Parse a delta string as found in the configuration files. """

    try:
        delta = _td()

        sign, elements, _ = __delta0_re.fullmatch(raw).groups()
        sign = (1, -1)[len(sign)]
        for res in __delta1_re.finditer(elements):
            num, typ = res.groups()
            num = int(num)

            if typ == 'w':
                delta += _td(weeks=sign * num)
            elif typ in 'jd':
                delta += _td(days=sign * num)
            elif typ == 'h':
                delta += _td(hours=sign * num)
            elif typ == 'm':
                delta += _td(minutes=sign * num)
            elif typ == 's':
                delta += _td(seconds=sign * num)
            else:
                raise Exception

        return delta
    except Exception:
        return None


def format_delta(td: _td) -> str:
    """ Create a delta string. """

    sls = zip(
        (_td(days=7), _td(days=1), _td(seconds=3600), _td(seconds=60)),
        'wdhm',
    )

    if td >= _td():
        d = ''

        for span, letter in sls:
            n = td // span
            if n:
                d += f'{n}{letter}'
                td -= span * n

        s = td.seconds
        if not d or s:
            d += f'{s}s'
    else:
        d = '-'

        for span, letter in sls:
            n = -td // span
            if n:
                d += f'{n}{letter}'
                td += span * n

        s = (-td).seconds
        if s:
            d += f'{s}s'

    return d


def make_delta(
    value: _Optional[_Union[str, int, float, _td]],
    allow_none: bool = False,
) -> _td:
    """ Make a delta from a raw value. """

    if value is None:
        if not allow_none:
            raise ValueError('must not be None')

    if isinstance(value, _td):
        return value

    try:
        value = int(value)
    except (TypeError, ValueError):
        if isinstance(value, str):
            new_value = parse_delta(value)
            if new_value is not None:
                return new_value

            raise ValueError(f'invalid time delta: {value!r}')

        raise TypeError(f'unknown type {type(value).__name__}')
    else:
        return _td(seconds=value)

# End of file.
