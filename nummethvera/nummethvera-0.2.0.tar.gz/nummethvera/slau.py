import csv
import numpy as np
import copy
from fractions import Fraction

def slau_inp_matr():
    """
    Функция возвращает матрицу, введённую пользователем с клавиатуры.

    Returns
    -------
    a : [[float, float, ...],
         [float, float, ...],
         ...]
        Матрица, введенная пользователем

    """
    while True:
        try:
            m = int(input('Сколько будет строк в матрице? '))
        except:
            print('Вы ввели не число')
        else:
            if m > 0:
                break
            else:
                print('Вы ввели не натуральное число') 

    while True:
        try:
            n = int(input('Сколько будет столбцов в матрице? '))
        except:
            print('Вы ввели не число')
        else:
            if n > 0:
                break
            else:
                print('Вы ввели не натуральное число')
                
    print("Введите элементы матрицы (заполнение идёт по строкам)")
    a = []
    for i in range(m):
        a.append([])
        for j in range(n):
            while True:
                try:
                    print(f'Введите элемент a[{i+1}][{j+1}]')
                    elem = eval(input())
                except:
                    print('Вы ввели не число')
                else:
                    break
            a[i].append(elem)
    return a



def csv_inp_matr(filename):
    """
    Функция импортирует матрицу из csv

    Parameters
    ----------
    filename : str
        Абсолютный или локальный путь до файла .csv

    Returns
    -------
    data : [[float, float, ...],
            [float, float, ...],
            ...]
        Матрица, импортированная из csv

    """
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    for i in range(len(data)):
        for j in range(len(data[0])):
            data[i][j] = eval(data[i][j])
    return data
    

def slau_outp_matr(a):
    """
    Функция для вывода матрицы

    Parameters
    ----------
    a : [[float, float, ...],
         [float, float, ...],
         ...]
        Матрица, введенная пользователем


    """
    for i in range(len(a)): 
        print(f'{a[i]}')      

def det(a):
    """
    Функция вычисляет определитель матрицы.

    Parameters
    ----------
    a : [[float, float, ...],
         [float, float, ...],
         ...]
        Матрица, определитель которой нужно вычислить.

    Raises
    ------
    ValueError
        Возникает, если введённая матрица a не квадратная

    Returns
    -------
    summ : float
        Определитель матрицы

    """
    if len(a) != len(a[0]):
        raise ValueError('Матрица должна быть квадратная')     
    for i in range(len(a)):
        summ = 0
        if len(a) == 1:
            summ += a[0][0]
            return summ
        else:
            for k in range(len(a)):
                b = copy.deepcopy(a)
                b.pop(0)
                for j in range(len(b)):
                    b[j].pop(k)
                summ += det(b)*((-1)**k)*int(a[0][k])
            return summ
        
        
def matrix_of_coefficients_is_square(a):
    """
    Функция показывает, является ли матрица квадртной.

    Parameters
    ----------
    a : [[float, float, ...],
         [float, float, ...],
         ...]
        Матрица, введенная пользователем

    Returns
    -------
    bool
        True - если матрица квадратная; 
        False - иначе

    """
    if len(a)+1 == len(a[0]):
        return True        
    return False

def norma(matr):
    """
    Функция вычисляет бесконечную норму матрицы.

    Parameters
    ----------
    matr : [[float, float, ...],
         [float, float, ...],
         ...]
        Матрица, введенная пользователем

    Returns
    -------
    float
        Максимальная из сумм всех столбцов - норма матрицы

    """
    matr = np.array(matr)
    return matr.sum(axis=0).max()



def ab(matr):
    """
    Функция разбивает введенную пользователем матрицу на две.

    Parameters
    ----------
    matr : [[float, float, ...],
         [float, float, ...],
         ...]
        Матрица, введенная пользователем

    Returns
    -------
    a : [[float, float, ...],
         [float, float, ...],
         ...]
        Квадратная матрица - левая часть введенной
    b : [float, float, ...]
        Правый столбец введенной матрицы

    """
    a = []
    b = []
    for i in range(len(matr)):
        a.append([])
        for j in range(len(matr[0])-1):
            a[i].append(matr[i][j])
    for i in range(len(matr)):
        b.append(matr[i][len(matr)])
    return a,b



def fix_diagonal(A):
    """
    Функция преобразовывает матрицу таким образом, чтобы на главной диагонали не было нулей.

    Parameters
    ----------
    A : [[float, float, ...],
         [float, float, ...],
         ...]
        Матрица, введённая пользователем

    Returns
    -------
    A : [[float, float, ...],
         [float, float, ...],
         ...]
        Преобразованная матрица A без 0 на главной диагонали

    """
    for i in range(len(A)):
        if (A[i][i] == 0):
            for j in range(len(A)):
                if A[j][i] != 0:
                    for k in range(len(A) + 1):
                        A[i][k] -= A[j][k]
                    break
    return A



def iakobi(A):
    """
    Функция находит решение системы линейных уравнений методом Якоби.

    Parameters
    ----------
    A : [[float, float, ...],
         [float, float, ...],
         ...]
        Матрица, введённая пользователем

    Returns
    -------
    A: [[float, float, ...],
        [float, float, ...],
        ...]
        Матрица коэффициентов изначальной матрицы A
    x: [float, float, ...]
        Список решений системы
    [[float, float, ...],
     [float, float, ...],
     ...]
        Обратная матрица для матрицы A
        
    """    
    B = []
    for i in range(len(A)):
        B.append([])
        B[i].append(A[i][-1])

    B1 = []
    for i in range(len(A)):
        B1.append(A[i][-1])
    for i in range(len(A)):
        A[i].pop(-1)
    tempx = [0 for i in range(len(A))]
    e = float(input('Введите эпсилон: '))
    x=[0 for i in range(0,len(A))]
    flag = True
    count = 0 
    while flag == True or count>100:
        for i in range(len(A)): 
            tempx[i] = B1[i]
            count +=1
            for j in range(len(A[i])):
                if i!=j:
                    count +=1
                    tempx[i] -= A[i][j]*x[j]
            tempx[i]/=A[i][i]
            count +=1
        flag = False
        for k in range(len(A)):
            if abs(x[k]-tempx[k])>=e:
                flag = True
            x[k] = tempx[k]
        if count > 100:
            break
    else:
        return A, x, np.linalg.inv(A), False

    return A, x, np.linalg.inv(A), True



def jdmethod(a, b):
    """
    Функция находит решение системы линейных уравнений методом Жордана-Гаусса.

    Parameters
    ----------
    a : [[float, float, ...],
         [float, float, ...],
         ...]
        Квадратная матрица - левая часть изначальной
    b : [float, float, ...]
        Правый столбец изначальной матрицы

    Returns
    -------
    b : [float, float, ...]
        Список решений системы
    a_orig : [[float, float, ...],
             float, float, ...],
             ...]
        Изначальная квадратная матрица

    """
    a = np.array(a, float)
    a_orig = copy.deepcopy(a)
    b = np.array(b, float)
    n = len(b)
    for k in range(n):
        if np.fabs(a[k,k]) < 1.0e-12:
            for i in range(k+1,n):
                if np.fabs(a[i,k]) > np.fabs(a[k,k]):
                    for j in range(k,n):
                        a[k,j],a[i,j] = a[i,j],a[k,j]
                    b[k],b[i] = b[i],b[k]
                    break
        pivot = a[k,k]
        for j in range(k,n):
            a[k,j] /= pivot
        b[k] /= pivot
        for i in range(n):
            if i == k or a[i,k] == 0: continue
            factor = a[i,k]
            for j in range(k,n):
                a[i,j] -= factor * a[k,j]
            b[i] -= factor * b[k]
            
    return b, a_orig



def linang_inv_jdmethod(a):
    """
    Функция находит обратную матрицу для введённой с помощью метода Жордана-Гаусса.

    Parameters
    ----------
    a : [[float, float, ...],
         [float, float, ...],
         ...]
        Изначальная матрица

    Returns
    -------
    [[float, float, ...],
     [float, float, ...],
     ...]
        Обратная матрица для введённой

    """
    a = np.array(a, float)
    e = np.eye(len(a))
    a = np.concatenate((a, e), axis=1)
    n = len(a)
    m = len(a[0])
    for k in range(n):
        if np.fabs(a[k,k]) < 1.0e-12:
            for i in range(k+1,n):
                if np.fabs(a[i,k]) > np.fabs(a[k,k]):
                    for j in range(k,m):
                        a[k,j],a[i,j] = a[i,j],a[k,j]
                    break

        pivot = a[k,k]
        for j in range(k,m):
            a[k,j] /= pivot

        for i in range(n):
            if i == k or a[i,k] == 0: continue
            factor = a[i,k]
            for j in range(k,m):
                a[i,j] -= factor * a[k,j]

    return a[:, n:]



def fraction_jbmethod(a):
    """
    Функция находит решение системы линейных уравнений методом Жордана-Гаусса,
    используя тип данных fraction

    Parameters
    ----------
    a : [[float, float, ...],
        [float, float, ...],
        ...]
        Изначальная матрица

    Returns
    -------
    x :[float, float, ...]
        Список решений системы

    """
    # Создание массива numpy размера n и инициализация нулем для хранения вектора решения
    n = len(a)
    x = np.zeros(n)

    # Чтение коэффициентов расширенной матрицы
    for i in range(n):
        for j in range(n+1):
            a[i][j] = Fraction(a[i][j])

    # Применение Метода Жордана-Гаусса
    for k in range(n):
        if np.fabs(a[k,k]) < 1.0e-12:
            for i in range(k+1,n):
                if np.fabs(a[i,k]) > np.fabs(a[k,k]):
                    for j in range(k,n+1):
                        a[k,j],a[i,j] = a[i,j],a[k,j]
                    break

        for j in range(n):
            if k != j:
                ratio = a[j][k]/a[k][k]

                for l in range(n+1):
                    a[j][k] = a[j][l] - ratio * a[k][l]

    # Получение решения
    for i in range(n):
        x[i] = a[i][n]/a[i][i]

    return x


def isdegenerate(A):
    """
    Функция проверяет, есть ли решения у введённой системы уравнений.

    Parameters
    ----------
    A : [[float, float, ...],
        [float, float, ...],
        ...]
        Введённая матрица

    Returns
    -------
    bool
        False - матрица не является вырожденной, корни есть.
        True - матрица вырожденная, либо не является квадратной, корней быть не может.

    """
    # ВВОД МАТРИЦЫ И ПРОВЕРКА НА ВЫРОЖДЕННОСТЬ 
    matr = np.array(A)
        
    DELTA = 0.01
    
    flag = True  # решение существует
    if matrix_of_coefficients_is_square(matr):
        a = ab(matr)[0]
        numpy_det = np.linalg.det(a)
        if abs(numpy_det) <= DELTA:
            my_own_det = det(a)
            if abs(my_own_det) <= DELTA:
                flag = False
            else:
                flag = True
        else:
            flag = True
            
        if flag:
            return False
        else:
            return True #матрица вырожденная, единого решения не существует
    else:
        return True #Матрица коэффициентов не является квадратной