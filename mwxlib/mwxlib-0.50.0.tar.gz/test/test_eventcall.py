#! python
# -*- coding: utf-8 -*-
import wx
import mwx
import unittest
from utilus import inspect_args

import platform
mwx.apropos(platform, '', pred=callable)


@inspect_args
def func(self, a, b, c=0, *args, **kwargs):
    """Test func"""
    print("(a,b,c) =", (a,b,c))
    pass


f = mwx.funcall(func)
print(inspect_args(f))

## f(None, -1) # TypeError: func() missing 1 required positional argument: 'b'
f(None, -1, -2) # ok
f(None, -1, -2, -3) # ok
f(None, -1, -2, -3, -4) # ok
