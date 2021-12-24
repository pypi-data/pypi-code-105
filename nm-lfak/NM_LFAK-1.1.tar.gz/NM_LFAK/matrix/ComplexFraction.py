from .Fraction import Fraction


class ComplexFraction:
    """
        Класс обертка для дробных расчетов над комплексными числами
    """
    def __init__(self, real: Fraction, imag: Fraction):
        self.real = real
        self.imag = imag

    @staticmethod
    def new_instance(x):
        if type(x) == ComplexFraction:
            return x
        if type(x) == Fraction:
            return ComplexFraction(x, Fraction.new_instance(0))
        if type(x) == int or type(x) == float:
            return ComplexFraction(Fraction.new_instance(x), Fraction.new_instance(0))
        if type(x) == complex:
            return ComplexFraction(Fraction.new_instance(x.real), Fraction.new_instance(x.imag))
        raise NotImplementedError(f'Type {type(x)} is not supported')

    def compute(self):
        return complex(self.real.compute(), self.imag.compute())

    def __neg__(self):
        return ComplexFraction(-self.real, -self.imag)

    def __add__(self, other):
        another = ComplexFraction.new_instance(other)
        return ComplexFraction(self.real+another.real, self.imag+another.imag)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        another = ComplexFraction.new_instance(other)
        return self + (-another)

    def __rsub__(self, other):
        return (-self) + other

    def __mul__(self, other):
        another = ComplexFraction.new_instance(other)
        return ComplexFraction(
            self.real * another.real - self.imag * another.imag,
            self.real * another.imag + another.real * self.imag
        )

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        another = ComplexFraction.new_instance(other)
        den = pow(another.real, 2) + pow(another.imag, 2)
        return ComplexFraction(
            (self.real * another.real + self.imag * another.imag) / den,
            (self.imag * another.real - self.real * another.imag) / den
        )

    def __rtruediv__(self, other):
        another = ComplexFraction.new_instance(other)
        return another / self

    def __pow__(self, power, modulo=None):  # сложная логика, лень писать
        return pow(self.compute(), power, modulo)

    def __rpow__(self, other):
        return pow(other, self.compute())

    def __abs__(self):
        return pow(pow(self.real, 2) + pow(self.imag, 2), 0.5)

    def __gt__(self, other):
        another = ComplexFraction.new_instance(other)
        return self.real > another.real and self.imag > another.imag

    def __lt__(self, other):
        another = ComplexFraction.new_instance(other)
        return self.real < another.real and self.imag < another.imag

    def __eq__(self, other):
        another = ComplexFraction.new_instance(other)
        return self.real == another.real and self.imag == another.imag

    def __str__(self):
        return f'ComplexFraction({self.real},{self.imag})'
