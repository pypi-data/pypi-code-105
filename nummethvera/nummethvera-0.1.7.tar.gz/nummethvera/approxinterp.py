import csv
from sympy import symbols, lambdify
import numpy as np
import math
import copy

def approxinterp_read_csv(filename):
    """
    Функция считывания данных из файла .csv 

    Parameters
    ----------
    filename : str
        Абсолютный или локальный путь к файлу.

    Returns
    -------
    x_list : [float, float, ...]
        Список координат х.
    y_list : [float, float, ...]
        Список координат у.
    n : int
        Длина выборки координат.

    """
    
    with open(filename, 'r') as file:
        data = csv.reader(file, delimiter=',')
        data = list(data)
        y_list = []
        x_list = []
        for i in range(len(data)):
            x_list.append(eval(data[i][0]))
            y_list.append(eval(data[i][1]))
    x_list = np.array(x_list)
    y_list = np.array(y_list)
    n = len(x_list)
    return x_list, y_list, n


def polinom_chebyshev(x_list, y_list, n):
    """
    Фильтрация выборки координа методом полинома Чебышева

    Parameters
    ----------
    x_list : [float, float, ...]
        Список координат х.
    y_list : [float, float, ...]
        Список координат у.
    n : int
        Длина выборки координат.

    Returns
    -------
    new_x_list : [float, float, ...]
        Новый список координат х.
    new_y_list : [float, float, ...]
        Новый список координат у.
    new_n : int
        Новая длина выборки координат.

    """
    
    new_n = n // 8
    new_index = sorted(list(set([round((np.math.cos((2 * k + 1) * np.math.pi / (2 * new_n + 2)) + 1) * (n - 1) / 2) for k in range(new_n)][::-1])))
    new_x_list = x_list[new_index]
    new_y_list = y_list[new_index]
    return new_x_list, new_y_list, new_n


def lagranje(x_list, y_list):
    """
    Интерполяция выборки методом Лагранжа

    Parameters
    ----------
    x_list : [float, float, ...]
        Список координат х.
    y_list : [float, float, ...]
        Список координат у.

    Returns
    -------
    new_L : function
        Интерполированная функция для введённой выборки.

    """
    
    x = symbols('x')
    L = 0
    l = []
    for j in range(len(x_list)):
        l.append(1)
        for k in range(len(x_list)):
            if k!=j:
                l[j] *= ((x-x_list[k])/(x_list[j]-x_list[k]))
        L += y_list[j]*l[j]
    new_L = lambdify(x, L)
    return new_L



def newton(x_list, y_list, interp_type=True):
    """
    Интерполяция выборки методом Ньютона

    Parameters
    ----------
    x_list : [float, float, ...]
        Список координат х.
    y_list : [float, float, ...]
        Список координат у.
    interp_type : bool, optional
        Тип интерполяции (вперёд\назад). 
        По умолчанию True - вперёд.
        False - назад.

    Raises
    ------
    ValueError
        Возникает при передаче не равноотстоящих узлов.

    Returns
    -------
    func : function
        Интерполированная функция для введённой выборки.

    """
    
    for i in range(len(x_list)-2):
        if abs((x_list[i+1] - x_list[i]) - (x_list[i+2] - x_list[i+1])) > 0.1 ** 12:
            raise ValueError('Данный метод применим только для равноотстоящих узлов!')
             
    #конечные разности
    d = []
    d.append(y_list)
    for i in range(len(y_list)-1):
        temp = d[i]
        d.append([])
        for j in range(len(temp)-1):
            d[i+1].append(temp[j+1]-temp[j])
        
    if interp_type: 
        #интерполяция вперед 
        x = symbols('x')
        h = x_list[1] - x_list[0]
        n = len(x_list)-1
        qv = (x - x_list[0])/h
        Pv = 0
        qspisv = []
        qspisv.append(1)
        for i in range(n):
            tmep = qspisv[i]
            qspisv.append(tmep*(qv-i))
    
        for i in range(n+1):
            Pv += qspisv[i]*d[i][0]/np.math.factorial(i)
    
        func = lambdify(x, Pv)

    else:
        #интерполяция назад
        x = symbols('x')
        h = x_list[1] - x_list[0]
        n = len(x_list)-1
        qn = (x - x_list[-1])/h
        Pn = 0
        qspisn = []
        qspisn.append(1)
        for i in range(n):
            tmep = qspisn[i]
            qspisn.append(tmep*(qn+i))
    
        for i in range(n+1):
            Pn += qspisn[i]*d[i][-1]/np.math.factorial(i)
    
        func = lambdify(x, Pn)
    return func



def jdmethod_fast(a):
    """
    Решение СЛАУ методом Жордана-Гаусса, используя numpy

    Parameters
    ----------
    a : [[float, float, ...],
         [float, float, ...],
         ...]
        Матрица, введённая пользователем.

    Returns
    -------
    [float, float, ...]
        Решение СЛАУ.

    """
    
    a = np.array(a, float)
    n = len(a)
    for k in range(n):
        if np.fabs(a[k,k]) < 1.0e-12:
            for i in range(k+1,n):
                if np.fabs(a[i,k]) > np.fabs(a[k,k]):
                    a[[i, k]] = a[[k, i]]
                    break
        pivot = a[k,k]
        a[k] = a[k] / pivot

        a[np.arange(n)!=k] -= a[np.arange(n)!=k][:, k].reshape((n-1, 1)) * a[k]
    return a[:, -1:]


def qubic_splines(x_list, y_list):
    """
    

    Parameters
    ----------
    x_list : [float, float, ...]
        Список координат х.
    y_list : [float, float, ...]
        Список координат у.

    Returns
    -------
    S : [function, function, ...]
        Список функций для каждого сплайна на указанном отрезке.

    """
    x = symbols('x')
    S = []
    a = y_list[:]
    b = []
    d = []
    number_of_splines = len(x_list)-1
    h = np.array(x_list[1:]) - np.array(x_list[:-1])
    C_to_solve = np.zeros((number_of_splines + 1, number_of_splines + 2))
    for j in range(number_of_splines + 1):
        if j == 0 or j == number_of_splines:
            C_to_solve[j][j] = 1
        else:
            C_to_solve[j][j - 1] = h[j - 1] / 3
            C_to_solve[j][j] = 2 * (h[j - 1] + h[j]) / 3
            C_to_solve[j][j + 1] = h[j] / 3
            C_to_solve[j][-1] = (y_list[j + 1] - y_list[j]) / h[j] - (y_list[j] - y_list[j - 1]) / h[j - 1]
    c = jdmethod_fast(C_to_solve).transpose()[0]
    for i in range(number_of_splines):
        d.append((c[i+1] - c[i])/(3*h[i]))
        b.append(((y_list[i+1]-y_list[i])/h[i]) - h[i]*(c[i+1]+2*c[i])/3)
        S.append(a[i] + b[i]*(x-x_list[i]) + c[i]*(x-x_list[i])*(x-x_list[i]) + d[i]*(x-x_list[i])*(x-x_list[i])*(x-x_list[i]))
    S.append(S[-1])
    return S


def linear_approximation(x_list, y_list):
    """
    Линейная аппроксимация выборки

    Parameters
    ----------
    x_list : [float, float, ...]
        Список координат х.
    y_list : [float, float, ...]
        Список координат у.

    Returns
    -------
    k : float
        Коэффициент k в уравнении y=kx+b 
    b : float
        Коэффициент b в уравнении y=kx+b 

    """
    summ1 = 0
    n = len(x_list)
    for i in range(len(x_list)):
        summ1 += x_list[i]*y_list[i]     
    summ2 = sum(x_list)*sum(y_list)
    k = (n*summ1 - summ2)/(n*sum([i**2 for i in x_list])-sum(x_list)**2)
    b = (sum(y_list)-k*sum(x_list))/n
    return k,b 


def dispersion_linear(x_list, y_list, k, b):
    """
    Функция находит дисперсию для линейной аппроксимации

    Parameters
    ----------
    x_list : [float, float, ...]
        Список координат х.
    y_list : [float, float, ...]
        Список координат у.
    k : float
        Коэффициент k в уравнении y=kx+b 
    b : float
        Коэффициент b в уравнении y=kx+b 

    Returns
    -------
    summ_d : float
        Дисперсия линейной аппроксимации

    """
    
    x_values = np.linspace(x_list[0], x_list[-1], num=len(x_list))
    y_values = np.poly1d([k, b])(x_values)
    summ_d = 0
    for i in range(len(x_list)):
        summ_d = (y_values[i] - y_list[i])**2
    return summ_d


def quadratic_approximation(x_list, y_list):
    """
    Аппроксимация квадратичной функцией

    Parameters
    ----------
    x_list : [float, float, ...]
        Список координат х.
    y_list : [float, float, ...]
        Список координат у.

    Returns
    -------
    x_koef : [float, float, float]
        Список из коэффициентов k1,k2,k3 в уравнении y=k1*x^2+k2*x+k3

    """
    n = len(x_list)
    summ_kv = 0
    for i in range(len(x_list)):
        summ_kv+= x_list[i]**2
    summ_cube = 0
    for i in range(len(x_list)):
        summ_cube+= x_list[i]**3
    summ_four = 0
    for i in range(len(x_list)):
        summ_four+= x_list[i]**4
    summ_xy = 0
    for i in range(len(x_list)):
        summ_xy += x_list[i]*y_list[i]
    summ_xkvy = 0
    for i in range(len(x_list)):
        summ_xkvy += (x_list[i]**2)*y_list[i]
    
    A = [[summ_kv, sum(x_list), n, sum(y_list)], [summ_cube, summ_kv, sum(x_list), summ_xy], [summ_four, summ_cube, summ_kv, summ_xkvy]]
    x_koef = jdmethod_fast(A).transpose()[0]
    return x_koef



def dispersion_quadratic(x_list, y_list, x_koef):
    """
    Функця находит дисперсию для квадратичной аппроксимации

    Parameters
    ----------
    x_list : [float, float, ...]
        Список координат х.
    y_list : [float, float, ...]
        Список координат у.
    x_koef : [float, float, float]
        Список из коэффициентов k1,k2,k3 в уравнении y=k1*x^2+k2*x+k3

    Returns
    -------
    summ_d : float
        Дисперсия линейной аппроксимации

    """
    x_values = np.linspace(x_list[0], x_list[-1], num=len(x_list))
    y_values = np.poly1d(x_koef)(x_values)
    summ_d = 0
    for i in range(len(x_list)):
        summ_d = (y_values[i] - y_list[i])**2
    return summ_d



def Gauss_approximation(x_list):
    """
    Аппроксимация методом Гаусса для формулы
    y_i = a * exp(-(x_i-b)^2/c^2)

    Parameters
    ----------
    x_list : [float, float, ...]
        Список координат х.

    Returns
    -------
    a : float
        Коэф а.
    b : float
        Коэф b.
    c : float
        Коэф c.
    """
    n = len(x_list)
    x__ = 1/n*(sum(x_list))
    p = 1/200
    summ_ = 0
    for i in range(len(x_list)):
        summ_ += (x_list[i] - x__)**2
    S_0 = math.sqrt((1/(n-1))*summ_)
    c = S_0/(math.sqrt(S_0))
    summ_E = 0
    for i in range(len(x_list)): 
        summ_E += x_list[i]*p
    b = summ_E
    a = 1/(c*(math.sqrt(2*math.pi)))
    return a, b, c



def dispersion_Gauss(x_list, y_list, a, b, c):
    """
    Дисперсия для аппроксимации методом Гаусса

    Parameters
    ----------
    x_list : [float, float, ...]
        Список координат х.
    y_list : [float, float, ...]
        Список координат у.
    a : float
        Коэф а уравненяи.
    b : float
        Коэф b уравненяи.
    c : float
        Коэф c уравненяи.

    Returns
    -------
    summ_d : float
        Дисперсия линейной аппроксимации

    """
    x_values = np.linspace(x_list[0], x_list[-1], num=len(x_list))
    y_values = [a*math.e**(-((x_i-b)**2)/(c**2)) for x_i in x_values]
    summ_d = 0
    for i in range(len(x_list)):
        summ_d = (y_values[i] - y_list[i])**2
    return summ_d