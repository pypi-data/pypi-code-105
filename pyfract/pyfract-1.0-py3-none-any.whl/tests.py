from fraction import Fraction

f = Fraction(1, 2)
print(f)
print(f.to_float())

f = Fraction(2, 4)
print(f.simplify())

print('-----')

f1 = Fraction(1, 2)
f2 = Fraction(1, 4)
print(f1 + f2)
print(f1 - f2)
print(f1 * f2)
print(f1 / f2)
print(f1 < f2)
print(f1 <= f2)
print(f1 > f2)
print(f1 >= f2)
print(f1 == f2)
print(f1 != f2)

print('-----')

print(Fraction.from_float(0.5))
print(Fraction.from_float_accurately(0.3333333333333333333))
x = Fraction.from_float_accurately(1.5325)
print(x)
print(x.to_float())
