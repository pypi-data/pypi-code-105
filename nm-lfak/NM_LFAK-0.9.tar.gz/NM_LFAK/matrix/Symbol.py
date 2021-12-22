from .Fraction import Fraction
from .ComplexFraction import ComplexFraction


class Symbol:
    """ Класс для символьных вычислений """
    def __init__(self, val='x'):
        self.val = val

    def __str__(self):
        return f'({self.val})'

    def __add__(self, other):
        val = f'({self.val}) + {other}'
        return Symbol(val)

    def __radd__(self, other):
        return self + other

    def __neg__(self):
        val = f'-({self.val})'
        return Symbol(val)

    def __sub__(self, other):
        val = f'({self.val} - {other})'
        return Symbol(val)

    def __rsub__(self, other):
        val = f'({other} - {self.val})'
        return Symbol(val)

    def __mul__(self, other):
        val = f'({self.val}) * {other}'
        return Symbol(val)

    def __rmul__(self, other):
        return self * other

    def __abs__(self):
        val = f'abs({self.val})'
        return Symbol(val)

    def get_function(self, *args):
        a = ','.join(args)
        return eval(f'lambda {a}: {self.val}', {'Fraction': Fraction, 'ComplexFraction': ComplexFraction})
