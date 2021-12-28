"""
Модуль для тестрирования polska,
при помощи библиотеки pytest
"""

from polska import __path__ as path
from polska.calculator import polska


def test_first_to_last():
    assert polska('1+2+3') == '12+3+'


def test_with_brackets():
    assert polska('(2+3)*3') == '23+3*'


def test_with_subtraction():
    assert polska('8-4*2') == '842*-'


def test_to_be():
    assert polska('3+9-1') == '39+1-'
