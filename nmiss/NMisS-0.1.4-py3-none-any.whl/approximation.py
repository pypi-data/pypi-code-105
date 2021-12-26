import pip

try:
    __import__('matplotlib')
except ImportError:
    pip.main([ 'install', 'matplotlib' ])

try:
    __import__('numpy')
except ImportError:
    pip.main([ 'install', 'numpy' ])

try:
    __import__('math')
except ImportError:
    pip.main([ 'install', 'math' ])

import numpy as np
import matplotlib.pyplot as plt
import math


def Crammer_method(matrix, vector):
    """
       Функция, которая решает СЛАУ методом Краммера

       :params matrix: матрица на вход

       :params vector: вектор свободных членов

       :return solution: решение СЛАУ
    """
    det = Determinant(matrix)
    if det != 0:
        matrix_a = [[], [], []]
        matrix_b = [[], [], []]
        matrix_c = [[], [], []]
        for i in range(len(matrix)):
            matrix_a[i].append(vector[i])
            matrix_a[i].append(matrix[i][1])
            matrix_a[i].append(matrix[i][2])

            matrix_b[i].append(matrix[i][0])
            matrix_b[i].append(vector[i])
            matrix_b[i].append(matrix[i][2])

            matrix_c[i].append(matrix[i][0])
            matrix_c[i].append(matrix[i][1])
            matrix_c[i].append(vector[i])

        solution = []
        solution.append(Determinant(matrix_a) / det)
        solution.append(Determinant(matrix_b) / det)
        solution.append(Determinant(matrix_c) / det)
        return solution
    else:
        solution = [0, 0, 0]
        return solution


def det2(matrix):  # определитель 2*2
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def minor(matrix, i, j):  # миноры матрицы
    tmp = [row for k, row in enumerate(matrix) if k != i]
    tmp = [col for k, col in enumerate(zip(*tmp)) if k != j]
    return tmp


def Determinant(matrix):  # определитель в целом поиск
    """
       Функция, которая находит определитель квадратной матрицы

       :params matrix: квадратная матрица

       :return number: определитель квадратной матрицы
    """
    if (len(matrix)) == (len(matrix[0])):
        size = len(matrix)
        if size == 2:
            return det2(matrix)
        return sum((-1) ** j * matrix[0][j] * Determinant(minor(matrix, 0, j))
                   for j in range(size))


def Lagrange(x_list, y_list, x0, x1, step):  # функция интерполяции лагранжа
    """
        Функция, которая аппроксимирует методом Лагранжа

        :params x_list: список из значений x

        :params y_list: список из значений y

        :params x0: начальная точка аппроксимации

        :params x1: конечная точка аппроксимации

        :params step: шаг аппроксимации

        :return Lagrange_massive_y, Lagrange_massive_x: аппроксимированные значения y, x
    """
    Lagrange_massive_x = []
    Lagrange_massive_y = []
    xx = x0
    for i in range(0, int((x1 - x0) / step) + 1):
        yy = 0
        if len(x_list) == len(y_list):
            for i in range(len(y_list)):
                L = 1
                for j in range(len(y_list)):
                    if i != j:
                        try:
                            L = L * (xx - x_list[j]) / (x_list[i] - x_list[j])
                        except ZeroDivisionError:
                            L = L * 1
                yy = yy + y_list[i] * L
            Lagrange_massive_y.append(yy)
            Lagrange_massive_x.append(xx)
            print('При x = ', xx, 'значение в точке = ', yy)
        xx = xx + step
    return Lagrange_massive_y, Lagrange_massive_x


def approximation_linear_func(list_x, list_y, x0, x1, step):  # аппроксимация линейной функцией
    """
        Функция, которая аппроксимирует линейной функцией

        :params x_list: список из значений x

        :params y_list: список из значений y

        :params x0: начальная точка аппроксимации

        :params x1: конечная точка аппроксимации

        :params step: шаг аппроксимации

        :return Linear_massive_x, Linear_massive_y: аппроксимированные значения x, y
    """
    Linear_massive_x = []
    Linear_massive_y = []
    xx = x0
    for r in range(0, int((x1 - x0) / step) + 1):
        s1 = 0;
        s2 = 0;
        s3 = 0;
        s4 = 0
        c1 = 1;
        c0 = 1
        yy = 0
        for i in range(len(x_list)):
            s1 = s1 + list_x[i] * list_x[i]
            s2 = s2 + list_x[i]
            s3 = s3 + list_x[i] * list_y[i]
            s4 = s4 + list_y[i]
        c1 = (s3 * len(list_x) - s2 * s4) / (s1 * len(list_x) - s2 * s2)
        c0 = (s1 * s4 - s2 * s3) / (s1 * len(list_x) - s2 * s2)
        yy = c0 + c1 * xx
        print('При x = ', xx, 'значение в точке = ', yy)
        Linear_massive_x.append(xx)
        Linear_massive_y.append(yy)
        xx = xx + step
    return Linear_massive_x, Linear_massive_y


def approximation_quadratic_func(list_x, list_y, x0, x1, step):  # аппроксимация квадратичной функцией
    """
         Функция, которая аппроксимирует квадратичной функцией

         :params x_list: список из значений x

         :params y_list: список из значений y

         :params x0: начальная точка аппроксимации

         :params x1: конечная точка аппроксимации

         :params step: шаг аппроксимации

         :return Quadratic_massive_x, Quadratic_massive_y: аппроксимированные значения x, y
    """
    Quadratic_massive_x = []
    Quadratic_massive_y = []
    xx = x0
    for r in range(0, int((x1 - x0) / step) + 1):
        a = [[], [], []]
        b = []
        s1 = 0;
        s2 = 0;
        s3 = 0;
        s4 = 0;
        s5 = 0;
        s6 = 0;
        s7 = 0;
        for i in range(len(x_list)):
            s1 = s1 + list_x[i] ** 4
            s2 = s2 + list_x[i] ** 3
            s3 = s3 + list_x[i] ** 2
            s4 = s4 + list_x[i]
            s5 = s5 + (list_x[i] ** 2) * list_y[i]
            s6 = s6 + list_x[i] * list_y[i]
            s7 = s7 + list_y[i]
        a[0].append(s1);
        a[0].append(s2);
        a[0].append(s3)
        a[1].append(s2);
        a[1].append(s3);
        a[1].append(s4)
        a[2].append(s3);
        a[2].append(s4);
        a[2].append(len(x_list))
        b.append(s5);
        b.append(s6);
        b.append(s7)
        a_1 = Crammer_method(a, b)  # пока вычисляю через numpy, потом поменяю
        yy = a_1[2] + a_1[1] * xx + a_1[0] * (xx ** 2)
        print('При x = ', xx, 'значение в точке = ', yy)
        Quadratic_massive_x.append(xx)
        Quadratic_massive_y.append(yy)
        xx = xx + step
    return Quadratic_massive_x, Quadratic_massive_y


def normal_distibution(list_x, list_y, x0, x1, step):
    """
         Функция, которая аппроксимирует функцией нормального распределения

         :params x_list: список из значений x

         :params y_list: список из значений y

         :params x0: начальная точка аппроксимации

         :params x1: конечная точка аппроксимации

         :params step: шаг аппроксимации

         :return normal_massive_x, normal_massive_y: аппроксимированные значения x, y
    """
    normal_massive_x = []
    normal_massive_y = []
    xx = x0
    a = [[], [], []]
    b = []
    s1 = 0;
    s2 = 0;
    s3 = 0;
    s4 = 0;
    s5 = 0;
    s6 = 0;
    s7 = 0;
    for i in range(len(x_list)):
        s1 = s1 + list_x[i] ** 4
        s2 = s2 + list_x[i] ** 3
        s3 = s3 + list_x[i] ** 2
        s4 = s4 + list_x[i]
        s5 = s5 + (list_x[i] ** 2) * list_y[i]
        s6 = s6 + list_x[i] * list_y[i]
        s7 = s7 + list_y[i]
    a[0].append(s1);
    a[0].append(s2);
    a[0].append(s3)
    a[1].append(s2);
    a[1].append(s3);
    a[1].append(s4)
    a[2].append(s3);
    a[2].append(s4);
    a[2].append(len(x_list))
    b.append(s5);
    b.append(s6);
    b.append(s7)
    a_1 = Crammer_method(a, b)  # пока вычисляю через numpy, потом поменяю
    print(a_1)
    for i in range(len(a_1)):
        if a_1[i] < 0:
            a_1[i] = a_1[i] * (-1)
    print(a_1)
    for r in range(0, int((x1 - x0) / step) + 1):
        try:
            yy = a_1[2] * math.e ** (-(((xx - a_1[1]) ** 2) / a_1[0] ** 2))
        except ZeroDivisionError:
            yy = 0
        normal_massive_x.append(xx)
        normal_massive_y.append(yy)
        xx = xx + step
    return normal_massive_x, normal_massive_y