import math as mmath

from .exception import *
from .objtype import objtype

class math:
    def increment(self, n):
        try:
            return n + 1
        
        except TypeError:
            raise InvalidTypeError("Object " + objtype(n) + " is not incrementable.")
            
    def double(self, n):
        try:
            return n * 2
        
        except TypeError:
            raise InvalidTypeError("Object " + objtype(n) + " is not incrementable.")
    
    def square(self, n):
        try:
            return n ** 2
        
        except TypeError:
            raise InvalidTypeError("Object " + objtype(n) + " is not incrementable.")
        
    def sqrt(self, n):
        try:
            if n == 0:
                return 0
            
            elif n < 0:
                return (-n ** 0.5) * 1j
            
            elif n > 0:
                return n ** 0.5
        
        except TypeError:
            raise InvalidTypeError("Object " + objtype(n) + " is not incrementable.")
    
    def factorial(self, n):
        if objtype(n) == "complex":
            raise NumberError("Complex numbers are not supported yet.")
        
        if n == 0:
            return 1
        
        elif n > 0:
            return mmath.gamma(n + 1)
        
        elif n < 0:
            return -mmath.gamma((-n) + 1)
        
    def b_round(self, n, a=0, *args, **kwargs):
        """Better rounding. More accurate."""
        return float(round(Decimal(str(n)), a, *args, **kwargs))
        
math = math()
