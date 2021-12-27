import pip

try:
    __import__('matplotlib')
except ImportError:
    pip.main([ 'install', 'matplotlib' ])

try:
    __import__('mpl_toolkits')
except ImportError:
    pip.main([ 'install', 'mpl_toolkits' ])

try:
    __import__('numpy')
except ImportError:
    pip.main([ 'install', 'numpy' ])

try:
    __import__('math')
except ImportError:
    pip.main([ 'install', 'math' ])

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
from math import factorial, exp, log, log10, log2, sqrt, pow, acos, asin, atan, pi, atan2, cos, sin, tan, cosh, sinh, \
    tanh, acosh, atanh


def Eulers_method(eq, a, b, h, x0, y0):  # метод Эйлера
"""
     Функция, которая решает дифференциальное уравнение методом Эйлера

     :params eq: уравнение y=* в типе str()

     :params a: нижнее значение

     :params b: верхнее значение

     :params h: шаг по решению

     :params x0: начальное значение x

     :params y0: начальное значение y

     :return x_mass, y_mass: значения x, y, являющиеся численным решением диффура
"""
    y_mass = []  # массив для рекурсивного подсчета y
    y_mass.append(y0)  # заносим y0 в массив
    x_mass = []  # массив для рекурсивного подсчета x
    x_mass.append(x0)  # заносим x0 в массив
    for i in range(1, int(((b - a) / h) + 1)):  # начинать цикл с 1 обязательно!
        y_mass.append(y_mass[i - 1] + h * eval_count(eq, x_mass[i - 1], y_mass[i - 1]))
        x_mass.append(x_mass[i - 1] + h)
    return x_mass, y_mass


def Eulers_Coshi_method(eq, a, b, h, x0, y0):  # метод Эйлера-Коши
"""
     Функция, которая решает дифференциальное уравнение методом Эйлера-Коши

     :params eq: уравнение y=* в типе str()

     :params a: нижнее значение

     :params b: верхнее значение

     :params h: шаг по решению

     :params x0: начальное значение x

     :params y0: начальное значение y

     :return x_mass, y_mass: значения x, y, являющиеся численным решением диффура
"""
    y_mass = []  # массив для рекурсивного подсчета y
    y_mass.append(y0)  # заносим y0 в массив
    x_mass = []  # массив для рекурсивного подсчета x
    x_mass.append(x0)  # заносим x0 в массив
    y_v_mass = []
    for i in range(1, int(((b - a) / h) + 1)):
        y_v_mass.append(y_mass[i - 1] + h * eval_count(eq, x_mass[i - 1], y_mass[i - 1]))
        x_mass.append(x_mass[i - 1] + h)
        y_mass.append(y_mass[i - 1] + ((h / 2) * (eval_count(eq, x_mass[i - 1], y_mass[i - 1])
                                                  + eval_count(eq, x_mass[i], y_v_mass[i - 1]))))
    return x_mass, y_mass


def Runge_Kutta_method(eq, a, b, h, x0, y0):  # метод Рунге-Кутта
    """
         Функция, которая решает дифференциальное уравнение методом Рунге-Кутта

         :params eq: уравнение y=* в типе str()

         :params a: нижнее значение

         :params b: верхнее значение

         :params h: шаг по решению

         :params x0: начальное значение x

         :params y0: начальное значение y

         :return x_mass, y_mass: значения x, y, являющиеся численным решением диффура
    """
    k1, k2, k3, k4 = [], [], [], []
    y_mass = []  # массив для рекурсивного подсчета y
    y_mass.append(y0)  # заносим y0 в массив
    x_mass = []  # массив для рекурсивного подсчета x
    x_mass.append(x0)  # заносим x0 в массив
    y_v_mass = []
    for i in range(1, int(((b - a) / h) + 1)):
        k1.append(eval_count(eq, x_mass[i - 1], y_mass[i - 1]))
        k2.append(eval_count(eq, (x_mass[i - 1] + h / 2), (y_mass[i - 1] + ((h * k1[i - 1]) / 2))))
        k3.append(eval_count(eq, (x_mass[i - 1] + h / 2), (y_mass[i - 1] + ((h * k2[i - 1]) / 2))))
        k4.append(eval_count(eq, (x_mass[i - 1] + h), (y_mass[i - 1] + (h * k3[i - 1]))))
        y_v_mass.append((h / 6) * (k1[i - 1] + 2 * k2[i - 1] + 2 * k3[i - 1] + k4[i - 1]))
        y_mass.append(y_mass[i - 1] + y_v_mass[i - 1])
        x_mass.append(x_mass[i - 1] + h)
    return x_mass, y_mass


def Adams_method(eq, a, b, h, x0, y0):
    """
         Функция, которая решает дифференциальное уравнение методом Адамса

         :params eq: уравнение y=* в типе str()

         :params a: нижнее значение

         :params b: верхнее значение

         :params h: шаг по решению

         :params x0: начальное значение x

         :params y0: начальное значение y

         :return x_mass, y_mass: значения x, y, являющиеся численным решением диффура
    """
    y_mass = []  # массив для рекурсивного подсчета y
    y_mass.append(y0)  # заносим y0 в массив
    x_mass = []  # массив для рекурсивного подсчета x
    x_mass.append(x0)  # заносим x0 в массив
    # вычислим первые 4 значения методом Рунге-Кутта
    for i in range(0, 3):
        x_mass, y_mass = Runge_Kutta_method(eq, a, b, h, x0, y0)
        x_mass = x_mass[:5]
        y_mass = y_mass[:5]
        for i in range(5, int(((b - a) / h) + 1)):
            y_mass.append(y_mass[i - 1] + (h / 24) * (
                    54 * eval_count(eq, x_mass[i - 1], y_mass[i - 1])
                    - 59 * eval_count(eq, x_mass[i - 2], y_mass[i - 2])
                    + 37 * eval_count(eq, x_mass[i - 3], y_mass[i - 3])
                    - 9 * eval_count(eq, x_mass[i - 4], y_mass[i - 4])))
            x_mass.append(x_mass[i - 1] + h)
    return x_mass, y_mass


def Eulers_method_system(a, b, h, x0, y0, z0, eq_1, eq_2):  # метод Эйлера для системы из 2 диффур
"""
     Функция, которая решает дифференциальное уравнение методом Эйлера

     :params a: нижнее значение

     :params b: верхнее значение

     :params h: шаг по решению

     :params x0: начальное значение x

     :params y0: начальное значение y

     :params z0: начальное значение z

     :params eq_1: уравнение в системе 1 в формате str()

     :params eq_2: уравнение в системе 2 в формате str()

     :return x_mass, y_mass, z_mass: значения x, y, z, являющиеся численным решением диффура
"""
    y_mass = []
    y_mass.append(y0)
    x_mass = []
    x_mass.append(x0)
    z_mass = []
    z_mass.append(z0)
    for i in range(1, int(((b - a) / h) + 1)):
        y_mass.append(y_mass[i - 1] + (h * (eval_count_z(eq_1, x_mass[i - 1], y_mass[i - 1], z_mass[i - 1]))))
        z_mass.append(z_mass[i - 1] + (h * (eval_count_z(eq_2, x_mass[i - 1], y_mass[i - 1], z_mass[i - 1]))))
        x_mass.append(x_mass[i - 1] + h)
    return x_mass, y_mass, z_mass


def Eulers_Coshi_method_system(a, b, h, x0, y0, z0, eq_1, eq_2):  # метод Эйлера-Коши для системы из 2 диффур
    """
         Функция, которая решает дифференциальное уравнение методом Эйлера-Коши

         :params a: нижнее значение

         :params b: верхнее значение

         :params h: шаг по решению

         :params x0: начальное значение x

         :params y0: начальное значение y

         :params z0: начальное значение z

         :params eq_1: уравнение в системе 1 в формате str()

         :params eq_2: уравнение в системе 2 в формате str()

         :return x_mass, y_mass, z_mass: значения x, y, z, являющиеся численным решением диффура
    """
    y_mass = []
    y_mass.append(y0)
    x_mass = []
    x_mass.append(x0)
    z_mass = []
    z_mass.append(z0)
    yv_mass = []
    zv_mass = []
    for i in range(1, int(((b - a) / h) + 1)):
        yv_mass.append(y_mass[i - 1] + (h * eval_count_z(eq_1, x_mass[i - 1], y_mass[i - 1], z_mass[i - 1])))
        zv_mass.append(z_mass[i - 1] + (h * eval_count_z(eq_2, x_mass[i - 1], y_mass[i - 1], z_mass[i - 1])))
        x_mass.append(x_mass[i - 1] + h)
        y_mass.append(y_mass[i - 1] + ((h / 2) * ((eval_count_z(eq_1, x_mass[i - 1], y_mass[i - 1], z_mass[i - 1])
                                                   + eval_count_z(eq_1, x_mass[i - 1], yv_mass[i - 1],
                                                                  zv_mass[i - 1])))))
        z_mass.append(z_mass[i - 1] + ((h / 2) * ((eval_count_z(eq_2, x_mass[i - 1], y_mass[i - 1], z_mass[i - 1])
                                                   + eval_count_z(eq_2, x_mass[i - 1], yv_mass[i - 1],
                                                                  zv_mass[i - 1])))))
    return x_mass, y_mass, z_mass


def Runge_Kutta_method_system(a, b, h, x0, y0, z0, eq_1, eq_2):  # метод Рунге-Кутты для системы из 2 диффур
    """
         Функция, которая решает дифференциальное уравнение методом Рунге-Кутта

         :params a: нижнее значение

         :params b: верхнее значение

         :params h: шаг по решению

         :params x0: начальное значение x

         :params y0: начальное значение y

         :params z0: начальное значение z

         :params eq_1: уравнение в системе 1 в формате str()

         :params eq_2: уравнение в системе 2 в формате str()

         :return x_mass, y_mass, z_mass: значения x, y, z, являющиеся численным решением диффура
    """
    y_mass = []
    y_mass.append(y0)
    x_mass = []
    x_mass.append(x0)
    z_mass = []
    z_mass.append(z0)
    k1, k2, k3, k4 = [], [], [], []
    l1, l2, l3, l4 = [], [], [], []
    for i in range(1, int(((b - a) / h) + 1)):
        k1.append(h * eval_count_z(eq_1, x_mass[i - 1], y_mass[i - 1], z_mass[i - 1]))
        l1.append(h * eval_count_z(eq_2, x_mass[i - 1], y_mass[i - 1], z_mass[i - 1]))
        k2.append(h * eval_count_z(eq_1, ((x_mass[i - 1]) + (h / 2)), ((y_mass[i - 1]) + (k1[i - 1] / 2)),
                                   ((z_mass[i - 1]) + (l1[i - 1] / 2))))
        l2.append(h * eval_count_z(eq_2, ((x_mass[i - 1]) + (h / 2)), ((y_mass[i - 1]) + (k1[i - 1] / 2)),
                                   ((z_mass[i - 1]) + (l1[i - 1] / 2))))
        k3.append(h * eval_count_z(eq_1, ((x_mass[i - 1]) + (h / 2)), ((y_mass[i - 1]) + (k2[i - 1] / 2)),
                                   ((z_mass[i - 1]) + (l2[i - 1] / 2))))
        l3.append(h * eval_count_z(eq_2, ((x_mass[i - 1]) + (h / 2)), ((y_mass[i - 1]) + (k2[i - 1] / 2)),
                                   ((z_mass[i - 1]) + (l2[i - 1] / 2))))
        k4.append(h * eval_count_z(eq_1, x_mass[i - 1], (y_mass[i - 1] + k3[i - 1]), (z_mass[i - 1] + l3[i - 1])))
        l4.append(h * eval_count_z(eq_2, x_mass[i - 1], (y_mass[i - 1] + k3[i - 1]), (z_mass[i - 1] + l3[i - 1])))
        y_mass.append(y_mass[i - 1] + (1 / 6 * (k1[i - 1] + 2 * k2[i - 1] + 2 * k3[i - 1] + k4[i - 1])))
        z_mass.append(z_mass[i - 1] + (1 / 6 * (l1[i - 1] + 2 * l2[i - 1] + 2 * l3[i - 1] + l4[i - 1])))
        x_mass.append(x_mass[i - 1] + h)
    return x_mass, y_mass, z_mass


def eval_count_z(eq, x, y, z):  # eval для системы
    try:
        a = eval(eq)
    except ZeroDivisionError:
        a = 0
    return a


def eval_count(eq, x, y):  # eval для обычного
    try:
        a = eval(eq)
    except ZeroDivisionError:
        a = 0
    return a


def eval_f(x, func):  # просто eval, вспомогательный для matprofi
    try:
        a = eval(func)
    except ZeroDivisionError:
        a = 0
    return a
