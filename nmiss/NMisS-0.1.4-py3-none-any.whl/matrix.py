  # в данной части кода мы пробуем импортировать библиотеки, и если их нет - устанавливаем и заново подключаем.
import pip

try:
    __import__('random')
except ImportError:
    pip.main([ 'install', 'random' ])

try:
    __import__('csv')
except ImportError:
    pip.main([ 'install', 'csv' ])

try:
    __import__('numpy')
except ImportError:
    pip.main([ 'install', 'numpy' ])

try:
    __import__('time')
except ImportError:
    pip.main([ 'install', 'time' ])

try:
    __import__('networkx')
except ImportError:
    pip.main([ 'install', 'networkx' ])

try:
    __import__('numpy')
except ImportError:
    pip.main([ 'install', 'numpy' ])

try:
    __import__('webbrowser')
except ImportError:
    pip.main([ 'install', 'webbrowser' ])

import random
import csv
import numpy as np
import time
import webbrowser


def Print_M(matrix):
    """
       Функция, которая выводит матрицу правильно.
       :params matrix: матрица на вход

       :return: матрица на выходе
    """
    for i in range(len(matrix)):
        print(matrix[i])


def Command_List():  # список команд для типа ввода матрицы
    print('\nВведите, каким способом вы хотите задать матрицу: ')
    a = input('1. Вручную \n2. CSV-файл \n3. Рандомная генерация\n0. Выход \nВведите команду: ')
    return a


def Input_M_T(strings, columns):
    """
       Функция, которая считывает матрицу, которую нужно транспонировать
       :params strings: количество строк в матрице

       :params colums: количество столбцов в матрице

       :return matrix_out: введенная матрица
    """
    # ввод с клавиатуры матрицы произвольной длины
    matrix_out = []
    print('Вводите значения строки через пробел: ')
    for i in range(strings):
        s = input()
        row = [x for x in s.split()]
        matrix_out.append(row)
    for i in range(len(matrix_out)):
        for j in range(len(matrix_out)):
            matrix_out[i][j] = matrix_out[i][j]
    return matrix_out


def Input_M(strings, columns):  # ввод с клавиатуры матрицы произвольной длины
    """
       Функция, которая считывает матрицу
       :params strings: количество строк в матрице

       :params colums: количество столбцов в матрице

       :return matrix_out: введенная матрица
    """
    matrix_out = []
    print('Вводите значения строки через пробел: ')
    while (True):
        is_complex = input('Если хотите вводить c комплексными числами, введите 1,  только действительные - 2: ')
        if is_complex == '1':
            print('Вводите значения строки через пробел: ')
            print('Вводите значения комплексного числа через запятую,пример: 1,2 = 1 + i*2')
            for i in range(strings):
                s = input()
                row = [x for x in s.split()]
                row2 = []
                for j in range(len(row)):

                    row3 = []
                    row3.append([float(x) for x in row[j].split(',')])
                    if len(row3[0]) == 1:
                        row3[0].append(0)
                    row2.append(complex(row3[0][0], row3[0][1]))
                matrix_out.append(row2)
            for i in range(len(matrix_out)):
                for j in range(len(matrix_out)):
                    matrix_out[i][j] = complex(matrix_out[i][j])
            return matrix_out
            return
            break
        elif is_complex == '2':
            print('Вводите значения строки через пробел: ')
            for i in range(strings):
                s = input()
                row = [float(x) for x in s.split()]
                matrix_out.append(row)
            for i in range(len(matrix_out)):
                for j in range(len(matrix_out)):
                    matrix_out[i][j] = float(matrix_out[i][j])
            return matrix_out
            break
        else:
            print('Неправильная команда')


def Gen_M(strings, columns):  # рандомная генерация матрицы по указанному кол-ву столбцов и строк
    """
       Функция, которая генерирует случайную матрицу n*m
       :params strings: количество строк в матрице

       :params colums: количество столбцов в матрице

       :return matrix: сгенерированная матрица
    """
    matrix = []
    for i in range(strings):
        row = []
        for j in range(columns):
            gen_num = random.randint(1, 20)
            row.append(gen_num)
        matrix.append(row)
    return matrix


def Addiction(matrix_1, matrix_2):  # сложение
    """
       Функция, которая складывает две матрицы
       :params matrix_1: матрица, первое слагаемое

       :params matrix_2: матрица, второе слагаемое

       :return matrix_out: введенная матрица
   """
    matrix_out = []
    for i in range(len(matrix_1)):
        if (len(matrix_1) == len(matrix_2)):
            if (len(matrix_1[i]) == len(matrix_2[i])):
                row = []
                for j in range(len(matrix_1[i])):
                    summ = matrix_1[i][j] + matrix_2[i][j]
                    row.append(summ)
                matrix_out.append(row)
            else:
                print('Разное кол-во столбцов')
        else:
            print('Разное кол-во строк')
    return matrix_out


def Substarction(matrix_1, matrix_2):  # вычитание
    """
       Функция, которая вычитает две матрицы
       :params matrix_1: матрица, уменьшаемое

       :params matrix_2: матрица, вычитаемое

       :return matrix_out: матрица, разность
   """
    matrix_out = []
    for i in range(len(matrix_1)):
        if (len(matrix_1) == len(matrix_2)):
            if (len(matrix_1[i]) == len(matrix_2[i])):
                row = []
                for j in range(len(matrix_1[i])):
                    summ = matrix_1[i][j] - matrix_2[i][j]
                    row.append(summ)
                matrix_out.append(row)
            else:
                print('Разное кол-во столбцов')
        else:
            print('Разное кол-во строк')
    return matrix_out


def Multiply_by_number(matrix_1, number):  # умножение матрицы на число
    """
       Функция, которая умножает матрицу на число
       :params matrix_1: матрица

       :params matrix_2: число, на которое необходимо умножить матрицу

       :return matrix_out: матрица, как результат
   """
    matrix_out = []
    for i in range(len(matrix_1)):
        row = []
        for j in range(len(matrix_1[i])):
            new_number = matrix_1[i][j] * number
            row.append(new_number)
        matrix_out.append(row)
    return matrix_out


def Multiply(matrix_1, matrix_2):  # умножение двух матриц, проверка на то, можно ли их умножить
    """
       Функция, которая умножает две матрицы
       :params matrix_1: матрица, первый множитель

       :params matrix_2: матрица, второй множитель

       :return matrix_out: произведение двух матриц
   """
    summ = 0
    row = []
    matrix_out = []
    if (len(matrix_1) == len(matrix_2[0])):
        for z in range(0, len(matrix_1)):
            for j in range(0, len(matrix_2[0])):
                for i in range(0, len(matrix_1[0])):
                    summ = summ + matrix_1[z][i] * matrix_2[i][j]
                row.append(summ)
                summ = 0
            matrix_out.append(row)
            row = []
        return matrix_out
    else:
        print('Данные матрицы нельзя перемножить. ')


def Transpose(matrix_1):  # транспонирование
    """
       Функция, которая транспонирует матрицу

       :params matrix_1: исходная матрица

       :return matrix_t: транспонированная матрица
   """
    matrix_t = []
    for j in list(range(len(matrix_1[0]))):
        row = []
        for i in list(range(len(matrix_1))):
            row.append(matrix_1[i][j])
        matrix_t.append(row)
    return (matrix_t)


def det2(matrix):  # определитель 2*2
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def minor(matrix, i, j):  # миноры матрицы
    tmp = [row for k, row in enumerate(matrix) if k != i]
    tmp = [col for k, col in enumerate(zip(*tmp)) if k != j]
    return tmp


def determinant(matrix):  # определитель в целом поиск
    """
       Функция, которая находит определитель квадратной матрицы

       :params matrix: квадратная матрица

       :return number: определитель квадратной матрицы
   """
    if (len(matrix)) == (len(matrix[0])):
        size = len(matrix)
        if size == 2:
            return det2(matrix)
        return sum((-1) ** j * matrix[0][j] * determinant(minor(matrix, 0, j))
                   for j in range(size))
    else:
        print('Это не квадратная матрица. Найти определитель невозможно. ')


def CSV_files_A():  # считываем матрицу A из CSV файла
    try:
        with open('Matrix_A.csv', encoding='utf-8-sig') as data_file:
            string_csv = []
            A = []
            for line in data_file:
                string_csv = line.strip().split(';')
                string_csv = [float(x) for x in string_csv]
                A.append(string_csv)
        return A
    except FileNotFoundError:
        print(
            'Перед выполнением операции с CSV файлами создайте в директории CSV-файл с названием Matrix_A.csv и перезапустите программу')


def CSV_files_A_T():  # считываем матрицу A из CSV файла
    try:
        with open('Matrix_A.csv', encoding='utf-8-sig') as data_file:
            string_csv = []
            A = []
            for line in data_file:
                string_csv = line.strip().split(';')
                string_csv = [x for x in string_csv]
                A.append(string_csv)
        return A
    except FileNotFoundError:
        print(
            'Перед выполнением операции с CSV файлами создайте в директории CSV-файл с названием Matrix_A.csv и перезапустите программу')


def CSV_files_B():  # считываем матрицу B из CSV файла
    try:
        with open('Matrix_B.csv', encoding='utf-8-sig') as data_file:
            string_csv = []
            B = []
            for line in data_file:
                string_csv = line.strip().split(';')
                string_csv = [float(x) for x in string_csv]
                B.append(string_csv)
        return B
    except FileNotFoundError:
        print(
            'Перед выполнением операции с CSV файлами создайте в директории CSV-файл с названием Matrix_B.csv и перезапустите программу')


# функции для проверки и сравнение по времени

def Transpose_NP(matrix):  # транспонирование с использованием numpy
    c0 = time.perf_counter()
    matrix.transpose()
    c1 = time.perf_counter()
    c2 = c1 - c0
    return c2


def Eval(c):  # считывание A+B*C и прочее
    cc = eval(c)
    return cc


def Determinant_NP(matrix):  # поиск детерминанта с использованием numpy
    c0 = time.perf_counter()
    np.linalg.det(matrix)
    c1 = time.perf_counter()
    c2 = c1 - c0
    return c2
