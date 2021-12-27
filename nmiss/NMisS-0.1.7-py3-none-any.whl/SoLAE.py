import pip

try:
    __import__('random')
except ImportError:
    pip.main(['install', 'random'])

try:
    __import__('numpy')
except ImportError:
    pip.main(['install', 'numpy'])

try:
    __import__('csv')
except ImportError:
    pip.main(['install', 'csv'])

try:
    __import__('copy')
except ImportError:
    pip.main(['install', 'copy'])

import copy
import random

# основные функции.

text_for_help = '0. Выход\nВыберите способ задания матрицы:\n1. Рандомная генерация\n2. CSV-файл\n3. Вручную\nВведите номер: '
matrix_example = [[1, 2, 3, 4],
                  [2, 3, 4, 5],
                  [3, 4, 5, 6]]


def Print_M(matrix):  # вывод матрицы построчно
    """
       Функция, которая выводит матрицу правильно.
       :params matrix: матрица на вход

       :return: матрица на выходе
    """
    for i in range(len(matrix)):
        print(matrix[i])


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


def symbols_gen(N):  # генерация списка из символов для красивого вывода матрицы.
    """
       Функция, которая генерирует символы для уравнений

       :params N: количество переменных

       :return symbols: сгенерированные символы, список
    """

    symbols = []
    for i in range(65, 65 + N):
        symbols.append(chr(i))
    return symbols


def beaty_output(matrix, matrix_ot, symbols):  # формирование строки уравнения и красивый вывод
    """
       Функция, которая выводит система уравнений
       :params matrix: матрица коэфициентов переменных

       :params matrix_ot: вектор свободных членов

       :params symbols: список символов для переменных

       :return eq_array: список с уравнениями, записанными правильно
    """

    eq_array = []
    for i in range(len(matrix_ot)):
        eq = ''
        for j in range(len(matrix[i])):
            eq_1 = str(matrix[i][j])
            if j == 0:
                eq = eq_1 + symbols[j]
            else:
                eq = eq + ' + ' + eq_1 + symbols[j]
        eq_2 = str(matrix_ot[i])
        eq = eq + ' = ' + eq_2
        eq_array.append(eq)
    for i in range(len(eq_array)):
        print(eq_array[i])
    return eq_array


def CSV_files_A():  # считываем матрицу A из CSV файла
    try:
        with open('Matrix_A.csv', encoding='utf-8-sig') as data_file:
            string_csv = []
            A = []
            for line in data_file:
                string_csv = line.strip().split(';')
                string_csv = [int(x) for x in string_csv]
                A.append(string_csv)
        return A
    except FileNotFoundError:
        print(
            'Перед выполнением операции с CSV файлами создайте в директории CSV-файл с названием Matrix_A.csv и перезапустите программу')


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
                for j in range(len(matrix_out[i])):
                    matrix_out[i][j] = float(matrix_out[i][j])
            return matrix_out
            break
        else:
            print('Неправильная команда')


def ways_of_inputing_matrix(number_of_way):  # способ задания матрицы для СЛАУ
    if number_of_way == '1':
        # Рандомная генерация.
        N = int(input('Введите кол-во переменных в исходной матрице: '))
        matrix_out = Gen_M(N, N + 1)
        matrix_ot, matrix_out = Vector_maker(matrix_out)
        symbols = symbols_gen(N)
        return matrix_out, matrix_ot, symbols

    elif number_of_way == '2':
        # CSV-считывание
        matrix_out = CSV_files_A()
        if len(matrix_out) == len(matrix_out[1]) - 1:
            matrix_ot, matrix_out = Vector_maker(matrix_out)
            symbols = symbols_gen(len(matrix_out))
            return matrix_out, matrix_ot, symbols
        else:
            print('Ошибка, в вашем файле матрица не соотвествует требованиям. Используем шаблонную матрицу. ')
            matrix_out = copy.deepcopy(matrix_example)
            matrix_ot, matrix_out = Vector_maker(matrix_out)
            symbols = symbols_gen(len(matrix_out))
            return matrix_out, matrix_ot, symbols

    elif number_of_way == '3':
        while True:
            strings = int(input('Введите кол-во строк в матрице: '))
            columns = int(input('Введите кол-во стобцов в матрице: '))
            if strings == columns - 1:
                matrix_out = Input_M(strings, columns)
                print(matrix_out)
                matrix_ot, matrix_out = Vector_maker(matrix_out)
                symbols = symbols_gen(strings)
                return matrix_out, matrix_ot, symbols
                break
            else:
                print('Кол-во строк должно быть на 1 меньше кол-ва столбцов. ')


def Vector_maker(matrix):
    """
       Функция, которая вычитает вектор из матрицы со всеми значениями СЛАУ

       :params matrix: матрица n*(n+1)

       :return matrix: матрица значений
       :return matrix_ot: вектор свободных членов
    """
    matrix_ot = []  # список из значений после "="
    for i in range(len(matrix)):  # заносим в список значения после "=" и обновляем нашу матрицу.
        matrix_ot.append(matrix[i][-1:])
        matrix[i] = matrix[i][:-1]
    return matrix_ot, matrix


def GJ(A, B):  # Гаусса-Жордана
    """
       Функция, которая решает СЛАУ методом Гаусса-Жордана

       :params A: матрица значений

       :params B: вектор свободных членов

       :return A: решенная матрица
    """
    A = join2(A, B)
    for i in range(len(A)):
        A[i] = [round(x / A[i][i], 3) for x in A[i]]  #
        a = [i for i in range(len(A))]
        a.remove(i)
        for j in a:
            A[j] = [x - A[i][A[j].index(x)] * A[j][i] for x in A[j]]
    return A


# Соединене двух матриц в одну
def join2(A, B):
    for i in range(len(A)):
        A[i].append(B[i][0])

    return (A)


def GJ2(A):  # обратная матрица
    E = []
    E = copy.deepcopy(A)
    for i in range(len(E)):
        # создание диагональеой матрицы с размерностью А
        for j in range(len(E[0])):
            if i == j:
                E[i][j] = 1
            else:
                E[i][j] = 0

    A = join(A, E)
    for i in range(len(A)):
        A[i] = [x / A[i][i] for x in A[i]]
        a = [i for i in range(len(A))]
        a.remove(i)
        for j in a:
            for x in range(0, len(A[j])):
                A[j][x] = A[j][x] - A[i][x] * A[j][i]
    return A


# Соединене двух матриц в одну
def join(A, E):
    for i in range(len(A)):
        for j in range(len(E[i])):
            A[i].append(E[i][j])

    return (A)


def Yakob(S, c):  # S - матрица с коэф, c - вектор свободных членов
    """
       Функция, которая решает СЛАУ методом Якоби

       :params S: матрица коэфициентов

       :params c: вектор свободных членов
    """
    # пока пихаем нули
    XXX0 = [0] * len(S)
    XXXd = []
    # диагональ
    for i in range(len(S)):
        XXXd.append(S[i][i])
        S[i][i] = 0
        c[0][i] = c[0][i] / XXXd[i]

    # список XXX - значения уравнений
    difference = []
    XXX = []
    HHH = []
    for i in c[0]:
        HHH.append(i)
        XXX.append(i)

    # создадим лист чтоб сохранять разницу по модулю

    XXX01 = []
    F = 3
    while F != 0:
        for i in range(len(S)):
            for j in range(len(S)):
                if j == 0:
                    XXX[i] = HHH[i] - S[i][j] * XXX0[j] / XXXd[i]
                else:
                    XXX[i] = XXX[i] - S[i][j] * XXX0[j] / XXXd[i]
            difference.append(abs(XXX[i] - XXX0[i]))
            XXX01.append(XXX[i])
        XXX0 = XXX01
        XXX01 = []
        for k in range(len(XXX0)):
            XXX0[k] = round(XXX0[k], 4)
            difference[k] = round(difference[k], 4)
        print(XXX0)
        print('Разница по модулю прошлой итерации XXX: ', difference)
        difference = []
        F -= 1


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