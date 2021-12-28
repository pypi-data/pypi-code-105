# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['impartial']
setup_kwargs = {
    'name': 'impartial',
    'version': '0.1.1',
    'description': 'A lightweight extension of functools.partial',
    'long_description': '# impartial\n\n[![build](https://github.com/georg-wolflein/impartial/workflows/build/badge.svg)](https://github.com/georg-wolflein/impartial/actions?query=workflow%3Abuild)\n[![PyPI](https://img.shields.io/pypi/v/impartial)](https://pypi.org/project/impartial)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/impartial)](https://pypi.org/project/impartial)\n[![Licence](https://img.shields.io/github/license/georg-wolflein/impartial)](https://github.com/georg-wolflein/impartial/blob/master/LICENSE)\n\n_impartial_ is a lightweight extension of [functools.partial](https://docs.python.org/3/library/functools.html#functools.partial) that allows modifying positional and keyword arguments in a functional style.\n\nThe main idea is that any function wrapped with `impartial` gets a method `with_<keyword>(value)` for every keyword argument of that function.\nEach `with_<keyword>(value)` method returns a new `impartial` function with that keyword being modified.\n\n```python\n>>> import impartial\n>>> @impartial\n... def power(x, exponent):\n...     return x ** exponent\n...\n>>> power\nimpartial(<function power at 0x10d54e790>)\n>>> square = power.with_exponent(2) # behaves like functools.partial(square, exponent=2)\n>>> square\nimpartial(<function power at 0x10d54e790>, exponent=2)\n>>> square(3)\n9\n```\n\nFeatures:\n\n- the `with_<keyword>(value)` methods can be arbitrarily **chained**\n- `impartial` functions are **immutable**: any "modification" of arguments returns a new `impartial` function\n- very **lightweight** (~50 LOC and no dependencies)\n- fully **compatible** with [functools.partial](https://docs.python.org/3/library/functools.html#functools.partial) (`impartial` is a subclass of `functools.partial`)\n- can be used as a **decorator**\n',
    'author': 'Georg Wölflein',
    'author_email': 'georgw7777@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/georg-wolflein/impartial',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
