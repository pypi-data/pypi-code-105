"""
Модуль для тестрирования polska,
при помощи библиотеки pytest
"""

from polska import __path__ as path
from polska.calculator import polska


def test_first_to_last():
    assert polska('1+2+3') == '12+3+'

