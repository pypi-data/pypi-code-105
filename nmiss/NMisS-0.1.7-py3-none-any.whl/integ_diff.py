import pip

try:
    __import__('mpmath')
except ImportError:
    pip.main([ 'install', 'mpmath' ])

try:
    __import__('math')
except ImportError:
    pip.main([ 'install', 'math' ])

try:
    __import__('numpy')
except ImportError:
    pip.main([ 'install', 'numpy' ])

from math import *
from mpmath import *
import numpy as np

mas1 = np.array([])
mas2 = np.array([])
mas3 = np.array([])
mas4 = np.array([])
mas5 = np.array([])
mas6 = np.array([])


def f(x, func):
    """
    Функция, которая возвращает значение f(x)
    :params x: значение x

    :params func: заданная функция в типе str()

    :return: значение в точке x.
    """
    try:
        a = eval(func)
    except ZeroDivisionError:
        a = 0
    return a


def fdx(x, h, func):
    """

    Функция, которая рассчитывает значение производной в конкретной точке методом двусторонней разности

    :params x: значение x
    :params h: шаг дифференцирования
    :params func: заданная функция в типе str()
    :return a: значение в дифференциале

    """

    try:
        a = (f(x + h, func) - f(x - h, func)) / (2 * h)
    except ZeroDivisionError:
        a = 0
    return a


def F(h, x, f):
    """

    Функция, которая рассчитывает значение интеграла в точке от x до x+шаг

    :params h: шаг дифференцирования
    :params func: заданная функция в типе str()
    :params x: значение x
    :return a: значение интеграла от x до (x+шаг)

    """

    try:
        a = (f(h) + f(x)) * (x - h) / 2
    except ZeroDivisionError:
        a = 0
    return a


def fdx(x, h, func):  # рассчет дифференциала от значения x с шагом h
    """
    Функция, которая рассчитывает значение производной в конкретной точке методом двусторонней разности.
    :params x: значение x

    :params h: шаг дифференцирования

    :params func: заданная функция в типе str()

    :return a: значение в дифференциале
    """
    try:
        a = (f(x + h, func) - f(x - h, func)) / (2 * h)
    except ZeroDivisionError:
        a = 0
    return a


def F(h, x, func):  # рассчет интеграла от значения шо на шо не пОнЯтНо, АнЯ оБъЯсНиТ
    """
    Функция, которая рассчитывает значение интеграла в точке от x до x+шаг.
    :params h: шаг дифференцирования

    :params func: заданная функция в типе str()

    :params x: значение x

    :return a: значение интеграла от x до (x+шаг)
    """
    try:
        a = (f(h) + f(x)) * (x - h) / 2
    except ZeroDivisionError:
        a = 0
    return a


def integ(a, b, step, func):  # рассчет интеграла и вывод результата
    """
    Функция, рассчитывающая интеграл от a до b

    :params a: нижний предел

    :params b: верхний предел

    :params step: шаг

    :params func: заданная функция в типе str()

    :return mas4: значение x
            mas5: значение интеграла в точке от x до x+шаг
            mas6: значение самой функции
    """
    inter = a + step
    mas4 = np.arange(int((b - a) / step) + 2)
    mas5 = np.arange(int((b - a) / step) + 2)
    mas6 = np.arange(int((b - a) / step) + 2)
    for i in range(1, int((b - a) / step)):  # (1)
        print('x =', round(inter, 3), 'f(x) =', round(f(inter, func), 3), "F(x) =", round(F(a, inter, func), 3))
        mas4[i] = inter
        mas5[i] = F(inter, step, func)
        mas6[i] = f(inter, func)
        inter = inter + step
    return mas4, mas5, mas6


def diff(a, b, step, func):  # рассчет дифференциала и вывод результата, когда a,b>0
    """
    Функция, рассчитывающая дифференциал от a до b

    :params a: нижний предел

    :params b: верхний предел

    :params step: шаг

    :params func: заданная функция в типе str()

    :return mas1: значение x
            mas2: значение производной в точке
            mas3: значение самой функции
    """
    inter = a  # шаг итерации функции или как это называется я хз
    mas1 = np.arange(int((b - a) / step) + 2)
    mas2 = np.arange(int((b - a) / step) + 2)
    mas3 = np.arange(int((b - a) / step) + 2)
    for i in range(1, int((b - a) / step) + 2):  # (1)
        print('x =', inter, 'f(x) =', f(inter, func), "f'(x) =", fdx(inter, step, func))
        mas1[i] = inter
        mas2[i] = fdx(inter, step, func)
        mas3[i] = f(inter, func)
        inter = inter + step
    return mas1, mas2, mas3