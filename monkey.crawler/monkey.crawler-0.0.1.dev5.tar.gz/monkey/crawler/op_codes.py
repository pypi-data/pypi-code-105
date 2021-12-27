#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from enum import Enum
import logging


class _TupleOpCode(namedtuple('TupleOpCode', ['name', 'plot_symbol', 'default_logging_level'])):

    def __str__(self):
        return f'({self.plot_symbol} -> {self.name} (with default logging level: {self.default_logging_level}'


class OpCode(Enum):
    INSERT = _TupleOpCode('INSERT', '+', logging.DEBUG)
    UPDATE = _TupleOpCode('UPDATE', '.', logging.DEBUG)
    IGNORE = _TupleOpCode('IGNORE', '_', logging.DEBUG)
    ERROR = _TupleOpCode('ERROR', 'X', logging.ERROR)
    CONFLICT = _TupleOpCode('CONFLICT', '!', logging.ERROR)
    DELETE = _TupleOpCode('DELETE', '#', logging.INFO)
    SKIP = _TupleOpCode('SKIP', '/', logging.DEBUG)
    RETRY = _TupleOpCode('RETRY', 'R', logging.INFO)
    NO_CHANGE = _TupleOpCode('NO_CHANGE', '=', logging.DEBUG)
    SUCCESS = _TupleOpCode('SUCCESS', '$', logging.DEBUG)
    UNDEFINED = _TupleOpCode('UNDEFINED', '?', logging.INFO)

    def get_plot_symbol(self) -> str:
        return self.value.plot_symbol

    def get_name(self) -> str:
        return self.value.name

    def get_default_logging_level(self) -> int:
        return self.value.default_logging_level


class OpCounter:

    def __init__(self):
        self.counters = {}
        self._total = 0

    def inc(self, op_code: OpCode, inc: int = 1):
        self.counters[op_code] = self.counters.get(op_code, 0) + inc
        self._total += inc

    def total(self, compute: bool = False):
        if compute:
            total = 0
            for op_code in self.counters.keys():
                total += self.counters[op_code]
            self._total = total
        return self._total

    def __str__(self):
        s = ''
        for op_code, count in self.counters.items():
            s += f'\t{op_code.name:<10}: {count:4}'
        return s


class Plotter:
    DEFAULT_MAX_COL = 100

    def __init__(self, max_col: int = DEFAULT_MAX_COL, head_len: int = 6):
        self.max_col: int = max_col
        self.plot_count: int = 0
        self.head_len: int = head_len

    @staticmethod
    def plot(op_code: OpCode):
        print(op_code.get_plot_symbol(), end='', flush=True)

    def print_line_head(self, op_count):
        if op_count % self.max_col == 0:
            print(f'\n{self.plot_count:<{self.head_len}}: ', end='', flush=True)
            self.plot_count += self.max_col

    def reset(self):
        self.plot_count = 0
