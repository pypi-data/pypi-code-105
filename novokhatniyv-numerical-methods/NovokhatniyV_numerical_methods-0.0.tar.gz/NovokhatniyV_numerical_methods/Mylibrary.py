# 1) create_matr:
#     the function creates a matrix
#     :param u: 1 if you yourself want to enter values into the matrix, and 2 if you want to enter random numbers
#     :param n: number of lines
#     :param m: numbers of columns
#     :return: matrix
# 2) task1st:
#     the function takes a matrix
#     returns the execution speed of a built-in python function
# 3) matrix_transpose:
#     the function creates a transposed matrix
#     :param n: number of lines
#     :param m: numbers of columns
#     :return: transposed matrix
# 4) plus:
#     addition of matrices only
#     fir - the first matrix
#     sec - the second matrix
#     d - matrix dictionary
#     returns the amount
# 5) subt:
#     subtraction of matrices only
#     fir - the first matrix
#     sec - the second matrix
#     d - matrix dictionary
#     returns the difference
# 6) mult:
#     matrix-by-number or matrix-by-matrix multiplication
#     fir - the first value
#     sec - second value
#     d - matrix dictionary
#     masmatr - list of matrices
#     returns the product
# 7) razn:
#     expr - expression
#     skobleft - array with left parenthesis indices
#     skobright - array with right parenthesis indices
#     d - matrix dictionary
#     masmatr - array of matrices
#     returns an expression without parentheses
# 8) matrix_expression:
#     counts matrix expression
#     SQUARE MATRIX ONLY
#     EVERY OPERATION MUST BE IN STAPLES
#     :param expr: matrix expression
#     :return: expression response
# 9) opr:
#     Takes a square matrix
#     The function is recursive
#     returns the determinant of a matrix
# 10) matrix_definer:
#     considers determinant
#     :param n: the number of rows of a square matrix or the matrix itself
#     :return: the determinant of a matrix
# 11) norm_matr:
#     calculates the matrix norm
#     :param matrix: matrix
#     :return: infinite matrix norm (i.e. max row sum)
# 12) obratn_matr:
#     counts the inverse of the matrix
#     :param matrix: square matrix
#     :return: inverse of the matrix
# 13) obratn_fract:
#     Takes a square matrix
#     Returns the inverse of a fraction
# 14) jacobi:
#     Jacobi method for calculating SLAEs
#     outputs:
#             matrix condition number
#             original matrix
#             answer
#             inverse matrix
#     :param matrixA: matrix of the system
#     :param matrixB: member matrix
#     :return: 1 if the system is solved and 0 if it is not solved
# 15) gauss:
#     Gauss-Jordan method for calculating SLAEs
#     outputs:
#             matrix condition number
#             original matrix
#             answer
#             inverse matrix
#     :param matrixA: matrix of the system
#     :param matrixB: member matrix
#     :return: 1 if the system is solved and 0 if it is not solved
# 16) gauss_drobi:
#     Gauss-Jordan method through the method of fractions for calculating the SLAE
#     outputs:
#             matrix condition number
#             original matrix
#             answer
#             inverse matrix
#     :param matrixA: matrix of the system
#     :param matrixB: member matrix
#     :return: 1 if the system is solved and 0 if it is not solved
# 17) slae:
#     function for calculating SLAE
#     :param n: dimension of the system matrix (can be changed)
#     :return: a string, whether a slough was counted or not
# 18) create_matrix:
#     creates a matrix
#     the first argument 'u' - 1 if you yourself want to enter values into the matrix,
#     and 2 if you want to enter random numbers
#     second argument 'n' is the number of rows and columns
# 19) f_current_way_power:
#     calculates the cost of the path
#     :param matrix: matrix
#     :param current_way: the path to be calculated
#     :return: route sum
# 20) f_new_way:
#     creates a new path by swapping 2 cities
#     :param current_way: path to be changed
#     :return: new way
# 21) simulated_annealing:
#     Simulated Annealing Algorithm
#     :param n: matrix dimension
#     :param tmax: initial temperature
#     :param tmin: final temperature
#     :return: best path, cost of the best path, and number of iterations


import random
import math
import time
import numpy as np
from fractions import Fraction as fr

def create_matr(u,n,m):
    """
    the function creates a matrix
    :param u: 1 if you yourself want to enter values into the matrix, and 2 if you want to enter random numbers
    :param n: number of lines
    :param m: numbers of columns
    :return: matrix
    """
    if u == '1':
        zzz = 0
        matrix = [[input("Введите {}-ый по строке и {}-ый по столбцу элемент: ".\
                         format(x+1,y+1))for y in range(m)] for x in range(n)]
        for i in range(n):
            for k in range(m):
                if 'j' in matrix[i][k]:
                    zzz = 1
        if zzz == 1:
            for i in range(n):
                for k in range(m):
                    xxx = 0
                    for h in matrix[i][k]:
                        if h == '-' or h == '+':
                            xxx+=1
                    if xxx == 1:
                        if '-' in matrix[i][k] and matrix[i][k].find('j') < matrix[i][k].find('-'):
                            znak = matrix[i][k].find('-')
                            matrix[i][k] = matrix[i][k][znak:]+'+'+matrix[i][k][:znak]
                        elif '+' in matrix[i][k] and matrix[i][k].find('j') < matrix[i][k].find('+'):
                            znak = matrix[i][k].find('+')
                            matrix[i][k] = matrix[i][k][znak:]+'+'+matrix[i][k][:znak]
                    elif xxx == 2:
                        if '+' in matrix[i][k] and matrix[i][k].find('j') < matrix[i][k].find('+'):
                            znak = matrix[i][k].find('+')
                            matrix[i][k] = matrix[i][k][znak:] + matrix[i][k][:znak]
                        elif matrix[i][k].find('j') < int(len(matrix[i][k]) + matrix[i][k].find('-', -1)):
                            znak = matrix[i][k].find('-',-1)
                            matrix[i][k] = '-'+matrix[i][k][znak:] + matrix[i][k][:znak-1]

                    matrix[i][k] = complex(matrix[i][k])
        else:
            for i in range(n):
                for k in range(m):
                    matrix[i][k] = float(matrix[i][k])

    elif u == '2':
        matrix = [[random.randrange(1,10) for y in range(m)] for x in range(n)]

    #print(matrix)
    return matrix

def task1st(matr):
    """
    the function takes a matrix
    returns the execution speed of a built-in python function
    """
    start_time = time.time()
    A = np.matrix(matr)
    #print(A)
    #print("--- %s seconds ---" % (time.time() - start_time))
    return time.time() - start_time

def matrix_transpose(n, m):
    """
    the function creates a transposed matrix
    :param n: number of lines
    :param m: numbers of columns
    :return: transposed matrix
    """

    u = input("Введите 1, если сами хотите ввести значения в матрицу, и 2 если хотите ввести рандомные числа: ")
    matrix = create_matr(u,n,m)
    matrixt = [[0 for y in range(n)] for x in range(m)]

    #timedef = task1st(matrix)
    #start_time = time.time()

    for x in range(n):
        for y in range(m):
            matrixt[y][x] = matrix[x][y]

    # вывод матрицы
    for x in range(m):
        for y in range(n):
            print(matrixt[x][y], end=' ')
        print('')

    #timemy = time.time() - start_time
    #print("--- %s seconds ---" % (time.time() - start_time))

    #if timedef == 0:
    #    return 'Функция выполняется слишком быстро чтобы точно посчитать разницу в скорости'
    return matrixt

#print("Задание 1 - транспонировать матрицу и сравнить со свтроенной функцией")
#print("Ответ: В {} раз встроенная функция быстрее (время моей разделил на время втсроенной)".format(task1(2, 2)))

def plus(fir, sec, d):
    """
    addition of matrices only
     fir - the first matrix
     sec - the second matrix
     d - matrix dictionary
     returns the amount
    """
    #print('сумма')
    fznach = d[fir]
    sznach = d[sec]
    s = len(fznach[0])

    matrix0 = [[0 for y in range(s)] for x in range(s)]


    for i in range(s):
        for j in range(s):
            matrix0[i][j] = fznach[i][j] + sznach[i][j]

    return matrix0

def subt(fir, sec, d):
    """
    subtraction of matrices only
     fir - the first matrix
     sec - the second matrix
     d - matrix dictionary
     returns the difference
    """
    #print('разность')
    fznach = d[fir]
    sznach = d[sec]
    s = len(fznach[0])

    matrix0 = [[0 for y in range(s)] for x in range(s)]

    for i in range(s):
        for j in range(s):
            matrix0[i][j] = fznach[i][j] - sznach[i][j]

    return matrix0

def mult(fir, sec, d, masmatr):
    """
    matrix-by-number or matrix-by-matrix multiplication
    fir - the first value
    sec - second value
    d - matrix dictionary
    masmatr - list of matrices
    returns the product
    """

    if fir not in masmatr and sec in masmatr:
        fznach = int(fir)
        sznach = d[sec]
        s = len(sznach[0])

        matrixmy = [[fznach for y in range(s)] for x in range(s)]
        matrix0 = [[0 for y in range(s)] for x in range(s)]

        for i in range(s):
            for j in range(s):
                matrix0[i][j] = sznach[i][j] * matrixmy[i][j]
        return matrix0
    else:
        fznach = d[fir]
        sznach = d[sec]
        s = len(sznach[0])

        matrix0 = [[0 for y in range(s)] for x in range(s)]

        for i in range(s):
            for j in range(s):
                matrix0[i][j] = sum([fznach[i][x] * sznach[x][j] for x in range(s)])

        return matrix0

def razn(expr, skobleft, skobright, d,masmatr):
    """
    expr - expression
    skobleft - array with left parenthesis indices
    skobright - array with right parenthesis indices
    d - matrix dictionary
    masmatr - array of matrices
    returns an expression without parentheses
    """
    razniz = 10000
    indi = 0
    indj = 0

    for i in range(len(skobleft)):
        for j in range(len(skobright)):
            if skobleft[i] < skobright[j] and skobright[j] - skobleft[i] < razniz:
                razniz = skobright[j] - skobleft[i]
                indi = skobleft[i]
                indj = skobright[j]

    ind = int((indj + indi) // 2)

    #вызов функций
    if expr[ind] == '+':
        for k in 'abcdefghklmnop':
            if k not in d:
                masmatr.append(k)
                d[k] = plus(expr[ind-2], expr[ind+2], d)
                break
    elif expr[ind] == '*':
        for k in 'abcdefghklmnop':
            if k not in d:
                masmatr.append(k)
                d[k] = mult(expr[ind - 2], expr[ind + 2], d, masmatr)
                break
    elif expr[ind] == '-':
        for k in 'abcdefghklmnop':
            if k not in d:
                masmatr.append(k)
                d[k] = subt(expr[ind-2], expr[ind+2], d)
                break

    expr = expr[:ind-4]+masmatr[-1]+expr[ind+5:]

    skobleft = [i for i, x in enumerate(expr) if x == '(']
    skobright = [i for i, x in enumerate(expr) if x == ')']
    #print(expr,11111111111)
    if len(skobright) > 0:
        expr = razn(expr, skobleft, skobright, d, masmatr)

    return expr

def matrix_expression(expr):
    """
    counts matrix expression
    SQUARE MATRIX ONLY
    EVERY OPERATION MUST BE IN STAPLES
    :param expr: matrix expression
    :return: expression response
    """
    masmatr = []
    d = {}
    for i in 'abcdefgh':
        if i in expr:
            masmatr.append(i)
            d[i] = 0
    #print(masmatr)
    kolvo = len(masmatr)
    #print(kolvo)
    n = int(input("Введите количество строк и столбцов для всех матриц: "))
    for i in range(kolvo):
        u = input("Матрица {}: Введите 1, если сами хотите ввести значения в матрицу, \
        и 2 если хотите ввести рандомные числа: ".format(masmatr[i]))
        matrix = create_matr(u,n,n)
        d[masmatr[i]] = matrix
    #print(d)

    #нахождение индексов скобок
    skobleft = [i for i, x in enumerate(expr) if x == '(']
    skobright = [i for i, x in enumerate(expr) if x == ')']

    expr = razn(expr, skobleft, skobright, d, masmatr)

    #print(len(expr))
    #print(expr)
    #print(d)
    return d[expr]

#print('Задание 2 - вычислить матричное выражение (каждая операция должна быть в скобочках)')
#print("Для примера возьмём выражение: '( ( ( a - b ) + ( 2 * b ) ) + ( a * b ) )'")
#print("Ответ: ", task2('( ( ( a - b ) + ( 2 * b ) ) + ( a * b ) )'))
#print("ОТВЕТ", task2('( a * b )'))

def opr(matrix):
    """
    Takes a square matrix
    The function is recursive
    returns the determinant of a matrix
    """
    n = len(matrix[0])
    #print('НОВЫЙ ЦИКЛ')
    #print('MAAAAAAAAAAAAAAAAAAAAAAATR',matrix)
    #print(n)
    if n > 1:
        if type(matrix[0][0]) == int:
            matrix0 = [[0 for y in range(n)] for x in range(n)]
            for i in range(n):
                for j in range(n):
                    if matrix[i][j] == 0:
                        matrix0[i][j] = 1
            #print('matrix0=',matrix0)

            summ = -1
            k = 0
            for i in range(n):
                if sum(matrix0[i]) > summ:
                    summ = sum(matrix0[i])

            #print('sum=',summ)

            summa = 100000000000
            for i in range(n):
                if sum(matrix0[i]) == summ and summa > sum(matrix[i]):
                    summa = sum(matrix[i])
                    k = i
        else:
            k = 0

        #print("Будем раскаладывать по {} строке (отсчет с 1)".format(k+1))

        ans = 0
        n = n - 1
        st = matrix[k]
        #print('k=', k)
        #print('st=', st)
        matrix.remove(matrix[k])
        #print('matrix=', matrix)
        for i in range(len(matrix[0])):
            matrixnew =[row[:(i)]+row[(i+1):] for row in matrix ]
            #print('matrixnew=', matrixnew)
            ans = ans + st[i]*(-1)**(k+1+i+1) * opr(matrixnew)

    else:
        return matrix[0][0]
    return ans

def matrix_definer(n):
    """
    considers determinant
    :param n: the number of rows of a square matrix or the matrix itself
    :return: the determinant of a matrix
    """
    if type(n) == int:
        u = input("Введите 1, если сами хотите ввести значения в матрицу, и 2 если хотите ввести рандомные числа: ")
        matrix = create_matr(u, n, n)
    else:
        matrix = [[0 for y in range(len(n[0]))] for x in range(len(n[0]))]
        for i in range(len(n[0])):
            for j in range(len(n[0])):
                matrix[i][j] = n[i][j]
        #matrix = n
    #print(matrix)
    return opr(matrix)

#print("Задание 3 - вычислить определитель матрицы (в примере вводится матрица 4 на 4)")
#print("ОТВЕТ: ", task3(4))

def norm_matr(matrix):
    """
    calculates the matrix norm
    :param matrix: matrix
    :return: infinite matrix norm (i.e. max row sum)
    """
    s = -1
    k = 0
    for j in range(len(matrix)):
        for i in range(len(matrix[0])):
            k += abs(matrix[j][i])
        if k > s:
            s = k
        k = 0
    return s

def obratn_matr(matrix):
    """
    counts the inverse of the matrix
    :param matrix: square matrix
    :return: inverse of the matrix
    """
    n = len(matrix[0])
    #создание расширенной матрицы
    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i].append(1)
            else:
                matrix[i].append(0)

    matrixnew = [[0 for i in range(2*n)] for j in range(n)]
    for i in range(n):
        for j in range(2*n):
            matrixnew[i][j] = matrix[i][j]
    #print('matrixnew',matrixnew)
    #j -строка i-cтолбцы
    for i in range(n):
        for j in range(n):
            for m in range(2 * n):
                matrix[i][m] = matrix[i][m] / matrixnew[i][i]
            #print('matr', matrix)
            for h in range(n):
                for g in range(2 * n):
                    matrixnew[h][g] = matrix[h][g]
            #print('matrixnew1', matrixnew)
            if i == j:
                for m in range(2*n):
                    matrix[i][m] = matrix[i][m] / matrixnew[i][i]
                #print('matr',matrix)
                for h in range(n):
                    for g in range(2 * n):
                        matrixnew[h][g] = matrix[h][g]
                #print('matrixnew1',matrixnew)
            else:
                for m in range(2*n):
                    matrix[j][m] = matrix[j][m] - matrixnew[i][m] * matrixnew[j][i]

                for h in range(n):
                    for g in range(2 * n):
                        matrixnew[h][g] = matrix[h][g]
                #print('matrixnew2',matrixnew)
    for i in range(n):
        matrix[i] = matrix[i][n:]
        for j in range(n):
            matrix[i][j] = round(matrix[i][j],7)
    return matrix

#print(obratn_matr([[2.6, -1.7, 2.5], [1.5, 6.2, -2.9], [2.8, -1.7, 3.8]]))
#a = [[2.6, -1.7, 2.5], [1.5, 6.2, -2.9], [2.8, -1.7, 3.8]]

#print(obratn_matr([[5, -3, 1], [-1, 6, -4], [1, -2, 5]]))

def obratn_fract(matrix):
    """
    Takes a square matrix
    Returns the inverse of a fraction
    """
    n = len(matrix[0])
    # создание расширенной матрицы
    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i].append(1)
            else:
                matrix[i].append(0)

    matrixnew = [[0 for i in range(2 * n)] for j in range(n)]
    for i in range(n):
        for j in range(2 * n):
            matrixnew[i][j] = matrix[i][j]
    # print('matrixnew',matrixnew)
    # j -строка i-cтолбцы
    for i in range(n):
        for j in range(n):
            for m in range(2 * n):
                matrix[i][m] = fr(matrix[i][m], matrixnew[i][i])
            # print('matr', matrix)
            for h in range(n):
                for g in range(2 * n):
                    matrixnew[h][g] = matrix[h][g]
            # print('matrixnew1', matrixnew)
            if i == j:
                for m in range(2 * n):
                    matrix[i][m] = fr(matrix[i][m], matrixnew[i][i])
                # print('matr',matrix)
                for h in range(n):
                    for g in range(2 * n):
                        matrixnew[h][g] = matrix[h][g]
                # print('matrixnew1',matrixnew)
            else:
                for m in range(2 * n):
                    matrix[j][m] = matrix[j][m] - matrixnew[i][m] * matrixnew[j][i]

                for h in range(n):
                    for g in range(2 * n):
                        matrixnew[h][g] = matrix[h][g]
                # print('matrixnew2',matrixnew)
    for i in range(n):
        matrix[i] = matrix[i][n:]
        for j in range(n):
            matrix[i][j] = round(matrix[i][j], 7)
    return matrix

def jacobi(matrixA, matrixB):
    """
    Jacobi method for calculating SLAEs
    outputs:
            matrix condition number
            original matrix
            answer
            inverse matrix
    :param matrixA: matrix of the system
    :param matrixB: member matrix
    :return: 1 if the system is solved and 0 if it is not solved
    """
    eps = 0.0003
    flag = 0
    n = len(matrixA[0])
    x0 = [0 for i in range(n)]
    x = [0 for i in range(n)]
    k = 0
    matrixA0 = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            matrixA0[i][j] = matrixA[i][j]


    #сам метод якоби
    while flag == 0:
        k+=1
        #print("----------------------------НОВЫЙ ЦИКЛ")
        x = [0 for i in range(n)]
        for i in range(n):
            for j in range(n):
                #print('------MATR', x)
                if i == j:
                    x[i] += matrixB[i][0]/matrixA[i][i]
                    #print('AAAAAAA',matrixB[i][0]/matrixA[i][i])
                    x[i] = round(x[i],7)
                    #print('x[i]',i,x[i])
                else:
                    x[i] -= (matrixA[i][j]*x0[j])/matrixA[i][i]
                    #print('AAAAAAA', matrixB[i][0] / matrixA[i][i])
                    x[i] = round(x[i], 7)
                    #print('x[i]', i, x[i])
        #print('x0',x0)
        #print('x',x)
        for i in range(n):
            #print(abs(x0[i]-x[i]),end = '')
            #print('')
            if k >= 100 and abs(x0[i]-x[i]) > 90:
                print("Метод Якоби расходится")
                print('Будем решать методом Гаусса-Жордана')
                return 0
            if abs(x0[i]-x[i]) <= eps:
                flag = 1
        # замена x на x0
        for i in range(n):
            x0[i] = x[i]


    cond = round(norm_matr(matrixA) * norm_matr(obratn_matr(matrixA)),4)
    #print('matrixA0',matrixA0)
    #print('matrixA',matrixA)
    #print('matrixB',matrixB)
    if cond < 100:
        print('Матрица хорошо обусловлена, ч.о.: ',cond)
        print('Исходная матрица: ',matrixA0)
        print("ОТВЕТ",x)
        print('Обратная матрица:', matrixA)
        return 1
    elif cond >= 100:
        print('Так как матрца плохо обусловлена, то применим метод Жордана-Гаусса')
        return 0

def gauss(matrixA, matrixB):
    """
    Gauss-Jordan method for calculating SLAEs
    outputs:
            matrix condition number
            original matrix
            answer
            inverse matrix
    :param matrixA: matrix of the system
    :param matrixB: member matrix
    :return: 1 if the system is solved and 0 if it is not solved
    """
    n = len(matrixA[0])
    matrixA0 = [[0 for j in range(n)] for i in range(n)] # исходная матрица
    for i in range(n):
        for j in range(n):
            matrixA0[i][j] = matrixA[i][j]
    matrixA1 = [[0 for j in range(n)] for i in range(n)] # обратная матрица
    for i in range(n):
        for j in range(n):
            matrixA1[i][j] = matrixA[i][j]

    for i in range(n):
        matrixA[i].append(matrixB[i][0]) #создание расширенной матрицы


    #сам метод Г-Ж
    #i - шаг в общем цыкле. m - шаг внутри общего цыкла, по строкам. j - шаг по столбцам
    for i in range(n):
        #print('NEW')
        diag_elem = matrixA[i][i]
        for m in range(i,n):
            our_elem = matrixA[m][i]
            if i == m:
                for j in range(n+1):
                    matrixA[m][j] = matrixA[m][j] / diag_elem
            else:
                for j in range(n+1):
                    matrixA[m][j] = matrixA[m][j] - matrixA[i][j] * our_elem
        for m in range(i):
            our_elem = matrixA[m][i]
            for j in range(n+1):
                matrixA[m][j] = matrixA[m][j] - matrixA[i][j] * our_elem
        #print(matrixA)
    #print('МОЯ',matrixA)
    #ответ
    x = [0 for i in range(n)]
    for i in range(n):
        x[i] = matrixA[i][n]
    #число обусловленности
    cond = round(norm_matr(matrixA1) * norm_matr(obratn_matr(matrixA1)), 4)
    #pinrt('x',x)
    #print('matrixA0', matrixA0)
    #print('matrixA', matrixA)
    #print('matrixB', matrixB)
    if cond < 100:
        print('Матрица хорошо обусловлена, ч.о.: ', cond)
        print('Исходная матрица: ', matrixA0)
        print("ОТВЕТ", x)
        print('Обратная матрица:', matrixA1)
        return 1
    elif cond >= 100:
        print('Так как матрца плохо обусловлена, то применим метод дробей')
        return 0

def gauss_drobi(matrixA,matrixB):
    """
    Gauss-Jordan method through the method of fractions for calculating the SLAE
    outputs:
            matrix condition number
            original matrix
            answer
            inverse matrix
    :param matrixA: matrix of the system
    :param matrixB: member matrix
    :return: 1 if the system is solved and 0 if it is not solved
    """
    n = len(matrixA[0])
    matrixA0 = [[0 for j in range(n)] for i in range(n)]  # исходная матрица
    for i in range(n):
        for j in range(n):
            matrixA0[i][j] = matrixA[i][j]
    matrixA1 = [[0 for j in range(n)] for i in range(n)]  # обратная матрица
    for i in range(n):
        for j in range(n):
            matrixA1[i][j] = matrixA[i][j]

    for i in range(n):
        matrixA[i].append(matrixB[i][0])  # создание расширенной матрицы
    # преобразование матрицы в дроби
    for i in range(n):
        for j in range(n+1):
            matrixA[i][j] = fr(matrixA[i][j])
    # сам метод Г-Ж для дробей
    # i - шаг в общем цыкле. m - шаг внутри общего цыкла, по строкам. j - шаг по столбцам
    for i in range(n):
        #print('NEW')
        diag_elem = matrixA[i][i]
        for m in range(i,n):
            our_elem = matrixA[m][i]
            if i == m:
                for j in range(n+1):

                    matrixA[m][j] = fr(matrixA[m][j], diag_elem)
            else:
                for j in range(n+1):
                    matrixA[m][j] = matrixA[m][j] - matrixA[i][j] * our_elem
        for m in range(i):
            our_elem = matrixA[m][i]
            for j in range(n+1):
                matrixA[m][j] = matrixA[m][j] - matrixA[i][j] * our_elem

    x = [0 for i in range(n)]
    for i in range(n):
        x[i] = matrixA[i][n]
    drob = int(input("Введите 1, если нужно округлить числа (до 5 знаков после запятой) и 2, \
    если округление не нужно и выведется полная дробь: "))
    if drob == 1:
        for i in range(n):
            x[i] = round(x[i],5)
            matrixA[i][n] = round(matrixA[i][n], 5)
    cond = round(norm_matr(matrixA1) * norm_matr(obratn_fract(matrixA1)), 4)
    #print('x',x)
    #print('matrixA0', matrixA0)
    #print('matrixA', matrixA)
    #print('matrixB', matrixB)

    if cond < 100:
        print('Матрица хорошо обусловлена, ч.о.: ', cond)
        print('Исходная матрица: ', matrixA0)
        print("ОТВЕТ", x)
        print('Обратная матрица:', matrixA1)
        return 1
    elif cond >= 100:
        print('После метода дробей матрица также плохо обусловленна, выведем получившиеся результаты')
        print('Матрица хорошо обусловлена, ч.о.: ', cond)
        print('Исходная матрица: ', matrixA0)
        print("ОТВЕТ", x)
        print('Обратная матрица:', matrixA1)
        return 0

def slae(n):
    """
    function for calculating SLAE
    :param n: dimension of the system matrix (can be changed)
    :return: a string, whether a slough was counted or not
    """
    n = int(input("Если хотите поменять размерность матрицы, то введите нужное число, \
    если не хотите, то введите 3: "))
    u = input("Введите 1, если сами хотите ввести значения в матрицу А (матрица системы), \
    и 2 если хотите ввести рандомные числа: ")
    matrixA = create_matr(u,n,n)
    u = input("Введите 1, если сами хотите ввести значения в матрицу B (столбец свободных членов), \
    и 2 если хотите ввести рандомные числа: ")
    matrixB = create_matr(u,n,1)
    #matrixA = [[5, -3, 1], [-1, 6, -4], [1, -2, 5]]
    #matrixB = [[3], [1], [4]]
    #matrixA = [[2.6, -1.7, 2.5], [1.5, 6.2, -2.9], [2.8, -1.7, 3.8]]
    #matrixB = [[3.7], [3.2], [2.8]]

    # создание еще одной матрицы А
    matrixA0 = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            matrixA0[i][j] = matrixA[i][j]

        # создание еще одной матрицы А
    matrixA1 = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            matrixA1[i][j] = matrixA[i][j]

    print('A', matrixA)
    print('B', matrixB)
    opredel = matrix_definer(matrixA)
    print("определитель равен: ",opredel)
    delta = 0.0007
    if float(abs(opredel)) <= delta:
        return "Определитель матрицы равен 0, следовательно данная матрица имеет бесконечность решений"
    else:
        print('Определитель матрицы не равен нулю следовательно система имеет решения')

    print('Сначала посчитаем методом Якоби')
    #a = jacobi(matrixA,matrixB)
    #if a == 0:
        #a = gauss(matrixA1,matrixB)
        #if a == 0:
        #    a = drobi(matrixA0,matrixB)
    a = gauss(matrixA1, matrixB)
    a = gauss_drobi(matrixA0, matrixB)
    return "СЛАУ посчиталась"

#print("посчитаем СЛАУ. В примере берется матрица системы 3 на 3")
#print(slae(3))

def create_matrix(u,n):
    """
    creates a matrix
    the first argument 'u' - 1 if you yourself want to enter values into the matrix,
    and 2 if you want to enter random numbers
    second argument 'n' is the number of rows and columns
    """
    if u == '1':
        matrixi = [[input("Введите {}-ый по строке и {}-ый по столбцу элемент: ".\
                          format(x+1, y+1))for y in range(n)] for x in range(n)]
    elif u == '2':
        mmin = int(input("Введите наименьшее число из дапозона рандомных чисел: "))
        mmax = int(input("Введите наибольшее число из дапозона рандомных чисел: "))
        matrixi = [[random.randint(mmin,mmax) for y in range(n)] for x in range(n)]
    return matrixi

def f_current_way_power(matrix, current_way):
    """
    calculates the cost of the path
    :param matrix: matrix
    :param current_way: the path to be calculated
    :return: route sum
    """
    n = len(matrix)
    summa = 0
    for i in range(n-1):
        summa += matrix[current_way[i]][current_way[i+1]]
    summa += matrix[current_way[-1]][current_way[0]]
    return summa

def f_new_way(current_way):
    """
    creates a new path by swapping 2 cities
    :param current_way: path to be changed
    :return: new way
    """
    first_value = random.randint(0,len(current_way)-1)
    second_value = random.randint(0,len(current_way)-1)
    while first_value == second_value:
        second_value = random.randint(0, len(current_way) - 1)

    current_way[first_value], current_way[second_value] = current_way[second_value], current_way[first_value]
    return current_way

def simulated_annealing(n, tmax=1000.0, tmin=0.01):
    """
    Simulated Annealing Algorithm
    :param n: matrix dimension
    :param tmax: initial temperature
    :param tmin: final temperature
    :return: best path, cost of the best path, and number of iterations
    """
    u = input("Введите 1, если сами хотите ввести значения в матрицу, и 2 если хотите ввести рандомные числа: ")
    matriwa = create_matrix(u, n)
    for i in range(n):
        print(matriwa[i])
    length = len(matriwa)
    first_way = list(range(0, length))
    start_time = time.time() #время
    the_best_way = first_way                                                 # лучший путь
    the_best_way_power = int(f_current_way_power(matriwa, the_best_way))     # лучшая мощность (min)

    k = 1
    tk = tmax

    # главный цикл
    while tk > tmin:
        tk = tmax /(1+k) # быстрый отжиг
        k += 1

        new_way = f_new_way(the_best_way) # создали новый путь
        new_way_power = int(f_current_way_power(matriwa, new_way))

        if new_way_power <= the_best_way_power:
            the_best_way = new_way
            the_best_way_power = new_way_power
        else:                                                           # считаем через температуру
            delta_s = new_way_power - the_best_way_power # смотрим разницу
            probability = 100 * math.exp(-delta_s/tk)
            random_probability = random.randint(0,100)
            if probability > random_probability:
                the_best_way = new_way
                the_best_way_power = new_way_power

    # переделывем the_best_way
    the_best_way_finish = ''
    for i in range(n):
        the_best_way_finish += str(the_best_way[i]) + '-'
    the_best_way_finish += str(the_best_way[0])

    return the_best_way_finish, the_best_way_power, k, time.time() - start_time

"""
1) По моему мнению метод Гаусса-Жорана в типе fraction лучше, потому что Якоби считает не все матрицы, 
не считает матрицы которые нельзя привести к диагональному преобразованию.
И мне кажется, что метод через дроби более точный чем обычный Г-Ж на каких-то супер огромных дробях, 
где из-за деления у нас точность падает, а тип fraction предотвращает это.
Но метод через дроби работает намного дольше чем обычный Г-Ж.
2) 
3) По моему мнению, использование типа fraction даёт выигрышь в точности при больших числах в обыкновенной дроби, 
но если числа обычные не очень маленькие, то лучше использовать Г-Ж.
   Если вводятся не переодические дроби, а десятичные, то fraction даёт выигрышь
"""