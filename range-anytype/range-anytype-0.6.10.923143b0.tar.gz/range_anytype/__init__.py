#!/usr/bin/env python
# coding=UTF-8

"""
range-anytype

Not an accurate Range for float. For best experience, you can use
decimal.Decimal or fractions.Fraction instead of float.
"""

try :
    object
except NameError :
    try :
        from range_anytype.py1compa import * # for Python 2.1 or earlier
    except ImportError :
        from rangeant.py1compa import * # for Python 2.1 or earlier
else :
    try :
        from range_anytype.py22plus import * # for Python 2.2 or newer
    except ImportError :
        from rangeant.py1compa import * # for Python 2.1 or earlier
