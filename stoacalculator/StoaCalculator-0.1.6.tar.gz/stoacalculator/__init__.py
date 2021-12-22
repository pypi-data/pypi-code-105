import math
import statistics
import matplotlib.pyplot as plt
import numpy as np
from sympy import *

# simple operations, basic aritmethic


def add_numbers(num1, num2):
    print(num1 + num2)


def substract_numbers(num1, num2):
    print(num1 - num2)


def multiply_numbers(num1, num2):
    print(num1 * num2)


def divide_numbers(num1, num2):
    print(num1 / num2)


def pow_numbers(num1, num2):
    print(num1 ** num2)


def sqr_root(num1):
    print(math.sqrt(num1))


# trigonometry
def sin(num1):
    print(math.sin(num1))


def cos(num1):
    print(math.cos(num1))


def tan(num1):
    print(math.tan(num1))


def acos(num1):
    print(math.acos(num1))


def asin(num1):
    print(math.asin(num1))


def atan(num1):
    print(math.atan(num1))

# Geometry circle (add radius)


def areacircle(num1):
    area = math.pi * num1 * num1
    print(area)

# Geometry rectangle (add height and width)


def arearectangle(num1, num2):
    area = num1 * num2
    print(area)

# Geometry square (add sides)


def areasquare(num1):
    area = num1 * num1
    print(area)

# Geometry triangle (add all sides)


def areasquare(num1, num2, num3):
    semiperimeter = (num1 + num2 + num3) / 2
    area = (semiperimeter*(semiperimeter-num1) *
            (semiperimeter-num2)*(semiperimeter-num3)) ** 0.5
    print(area)

# Statistics


def mean(list):
    print(statistics.mean(list))


def median(list):
    print(statistics.median(list))


def mode(list):
    print(statistics.mode(list))

# Plotting


def linearplot(x, linearformula):

    plt.style.use('dark_background')

    # setting the axes at the centre
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.title('Stoas Calculator Graph')
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_color('#00FFFF')
    ax.spines['bottom'].set_color('#00FFFF')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # plot the function
    plt.plot(x, linearformula, 'w', label='Equation')

    plt.legend(loc='upper left')

    # show the plot
    plt.show()


def quadraticplot(x, quadraticformula):

    plt.style.use('dark_background')

    # setting the axes at the centre
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.title('Stoas Calculator Graph')
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_color('#00FFFF')
    ax.spines['bottom'].set_color('#00FFFF')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # plot the function
    plt.plot(x, quadraticformula, 'w', label='Equation')

    plt.legend(loc='upper left')

    # show the plot
    plt.show()


def cubicplot(x, cubicformula):

    plt.style.use('dark_background')

    # setting the axes at the centre
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.title('Stoas Calculator Graph')
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_color('#00FFFF')
    ax.spines['bottom'].set_color('#00FFFF')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # plot the function
    plt.plot(x, cubicformula, 'w', label='Equation')

    plt.legend(loc='upper left')

    # show the plot
    plt.show()


def trigonometricplot(x, trigonometricformula):

    plt.style.use('dark_background')

    # setting the axes at the centre
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.title('Stoas Calculator Graph')
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_color('#00FFFF')
    ax.spines['bottom'].set_color('#00FFFF')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # plot the function
    plt.plot(x, trigonometricformula, 'w')

    # show the plot
    plt.show()


def exponentialplot(x, exponentialformula):

    plt.style.use('dark_background')

    # setting the axes at the centre
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.title('Stoas Calculator Graph')
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_color('#00FFFF')
    ax.spines['bottom'].set_color('#00FFFF')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # plot the function
    plt.plot(x, exponentialformula, 'w')

    # show the plot
    plt.show()


def biplot(x, formula1, formula2):

    plt.style.use('dark_background')

    # setting the axes at the centre
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.title('Stoas Calculator Graph')
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_color('#00FFFF')
    ax.spines['bottom'].set_color('#00FFFF')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # plot the function
    plt.plot(x, formula1, 'w', label='1st Equation')
    plt.plot(x, formula2, 'm', label='2nd Equation')

    plt.legend(loc='upper left')

    # show the plot
    plt.show()


def derivatives(function):
    print(diff(function))


def integrals(function):
    print(integrate(function))

def GCM(num1, num2):
    print(math.gcd(num1,num2))

def LCM(num1, num2):
    print(math.lcm(num1,num2))

def D2F(num1):
    print((num1).as_integer_ratio())
