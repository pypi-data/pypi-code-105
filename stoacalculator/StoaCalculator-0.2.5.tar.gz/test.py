import math


def taylor(num1, num2):
    sine = 0
    for i in range(num2):
        sign = math.pow(-1, i)
        pi = math.pi
        a = num1*(pi/180)
        sine = sine+(sign*(a**(2.0*i+1))/math.factorial(2*i+1))
    print(sine)
    return sine

taylor(90, 5)