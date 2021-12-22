from pandas import read_csv
from scipy.linalg import solve
import matplotlib.pyplot as plt
import numpy as np
from sympy import simplify, expand, Symbol
from numpy import vstack, array, polyfit, array, dot, linalg, arange, reshape 
from math import log, exp


def reading_csv(path, header = False, delimiter = ','):
    """Считывание X, Y из файла
    
    path - путь к файлу
    header - заголовки
    delimiter - разделитель"""
    
    
    
    if header:
        points = read_csv(path, names = header, sep = delimiter)
        return [i for i in points[list(points)[0]]], [i for i in points[list(points)[1]]]
    else:
        points = read_csv(path, sep = delimiter)

        return [i for i in points[list(points)[0]]], [i for i in points[list(points)[1]]]
    
    
def factor(n):
    """Факториал N
    return N!"""
    r = 1
    for i in range(1,n+1):
        r = r*i   
    return r

def check_step(x):
    """Проверка Шага выборки"""
    s = x[1] - x[0]
    return s
    
def mnogochlen(x, y):
    """Функция принимающая x, y и выдающая ответ
    
    x - x
    y - y"""
    
    
    main_mtrx = []
    for i in x:
        main_mtrx.append([i**(el) for el in range(len(x))])
    main_mtrx = array(main_mtrx)
    y = [[i] for i in y]
    y = array(y)
    answ = solve(main_mtrx, y)
    
    return answ    

def answer(x, y, answ, flag):
    """Выдает ответ, и Многочлен
    x, y = x, y
    answ - ответ 
    flag - влияет на выдачу ответа
    Либо просто x, y 
    либо график"""
    
    h = ''
    answ = [float(el[0]) for el in answ]
    
    for ind, el in enumerate(answ[::-1]):
        h += f'+{el}*(x**{len(answ) - ind-1})'
    x1 = []
    y1 = []
    for i in range(int(min(x))*10, int(max(x))*10 + 1):
        x1.append(i/10)
        y1.append(eval(h.replace('x', str(i/10))))
    if flag:
        print('Многочлен: ' + h)
        for ind, el in enumerate(x):
            print('x: '+ str(el)+' '+'y: '+ str(y[ind])+ ' ' + 'fi: ' + str(round(eval(h.replace('x', str(el))))))

        plt.scatter(x, y)
        plt.plot(x1,y1)
    else:
        return [x1, y1] 
    
def lagr(path, header = False, delimiter = ',', flag = True):
    
    """Объединение метода Answer, для красоты
    
    x, y = x, y
    answ - ответ 
    flag - влияет на выдачу ответа
    Либо просто x, y 
    либо график
    """
    
    x, y = reading_csv(path = path, delimiter = delimiter)
    return answer(x, y, mnogochlen(x, y), flag = flag)

def table(x, y):
    """строит таблицу ньютона для вычисления кэфов методом Ньютона
    
    x, y = x, y
    """
    
    table1 = [[0 for j in range(len(x))] for i in range(len(x)+1)]
    table1[0], table1[1] = x, y 
    for ind, el in enumerate(table1[2:]):
        for i in range(len(el)-ind-1):
            table1[ind+2][i] = -(table1[ind+1][i] - table1[ind+1][i+1])
    table1 = np.array(table1).T
    return table1



def newton_F(x, y, table):
    """Функция Ньютон вперед
    
    X, Y = X, Y
    table - Таблица Ньютона (метод table)
    
    return - многочлен Ньютона
    """
    
    P = ''
    h = check_step(x)
    
    for i in range(1, len(y) + 1):
        skobochki = ''
        for j in range(1, i):
            skobochki += f'*(x - {table[j-1][0]})'
            
        helpi = f'{table[0][i]}/({factor(i-1)}*{h**(i-1)})'
        if i == 1:
            P += f'({helpi}){skobochki}'
        else:
            P += f'+({helpi}){skobochki}'
            

    return P

def newton_S(x, y, table):
    """Функция Ньютон назад
    
    X, Y = X, Y
    table - Таблица Ньютона (метод table)
    
    return - многочлен Ньютона"""

    from sympy import simplify, expand, Symbol
    P = ''
    h = check_step(x)
    
    for i in range(1, len(y)+1):
        skobochki = ''
        for j in range(1, i):
            skobochki += f'*(x - {table[len(y)-j][0]})'
        
        helpi = f'{table[len(y) - i][i]}/({factor(i-1)}*{h**(i-1)})'
        if i == 1:
            P += f'({helpi}){skobochki}'
        else:
            P += f'+({helpi}){skobochki}'

    return P
            
            
def newton(path, header = False, delimiter = ',', FoS = 'F', flag = True):
    """
    Функция объединяющая эти два метода (Newton_F, Newton_S)
    в один посредствам флага 

    path - Путь к X, Y
    
    """
    
    x, y = csv(path = path, delimiter = delimiter)
    if FoS == 'F':
        F = newton_F(x, y, table(x, y))
    if FoS == 'S':
        F = newton_S(x, y, table(x, y))
    

    x1 = []
    y1 = []
    for i in range(int(min(x))*10, int(max(x))*10+1):
        x1.append(i/10)
        y1.append(eval(F.replace("x", str(i/10))))

    if flag:
        for ind, el in enumerate(x):
            print('x: '+ str(el)+' '+'y: '+ str(y[ind])+ ' ' + 'fi: ' + str(eval(F.replace("x", str(i/10)))))
        print(F)
        
        plt.plot(x1,y1)
        plt.scatter(x, y)
    else:
        return [x1, y1]

def search_C(x, y):
    
    """ Поиск С по формуле и
    генерируемой таблице
   
    x, y = x, y"""
    
    
    h = check_step(x)
    X = [[4*h if i == j else 0 for j in range(len(x)-2)]for i in range(len(x) - 2)]
    
    for i in range(len(X)):
        try:
            X[i][i+1] = h
        except:
            pass
        try:
            X[i+1][i] = h
        except:
            pass
    
    Y = [[(3/h)*(y[i+2]-2*y[i+1]+y[i])] for i in range(len(x)-2)]
    
    return vstack(([0],array(solve(X,Y))))


def search_ABD(x, y, c):
    
    """Поиск Остальных кэфов через С
    x, y = x, y 
    c = search_C(x, y)
    """
    h = check_step(x)
    
    c = [float(el[0]) for el in c]
    c += [0]
    a = y[:-1]
    d = [(c[i+1]-c[i])/3*h for i in range(len(c)-1)] 
    
    b = [(y[i]-y[i-1])/h-(c[i+1]+2*c[i])*h/3 for i in range(len(c)-1)]
    del c[-1]
    
    return [a,b,c,d]

def splain(path):
    """Генерация формул и вычисление значений в точках
    path - путь к x, y
    """
    x, y = csv(path)
    
    abcd = search_ABD(x, y, search_C(x, y))[::-1]
    for i in range(len(abcd[0])):
        helpi = f'{abcd[0][i]}*(x-{x[i]})**3+{abcd[1][i]}*(x-{x[i]})**3+{abcd[2][i]}*(x-{x[i]})**3+{abcd[3][i]}'
        print('x: '+str(x[i+1])+' '+'y: '+str(y[i])+' fi: '+str(eval(helpi.replace('x', str(x[i]))))+"  "+helpi)
        

def kx(path,delim = ',', flag = True):
    """Апроксимация Прямой
    
    path - Путь к x, y
    flag - Влияет на вывод ответа
    Либо Просто точки,
    Либо Графики"""
    x, y = csv(path, delimiter=delim)
    
    
#     Решаем слау для поиска кэфов
    kx = solve([[sum([i**2 for i in x]),sum(x)],[sum(x), len(x)]],[[sum([y[i]*x[i] for i in range(len(x))])],[sum(y)]])
    x1 = []
    y1 = []
#     генерируем точки
    for i in range(int(min(x)), int(max(x))+1):
        x1.append(i)
        y1.append(kx[0][0]*i+kx[1][0])
#         выводим
    if flag: 
        print(f'y = {kx[0][0]}x+{kx[1][0]}')
        print()
        for ind, el in enumerate(x):
            print(f'x:{el} y:{y[ind]} fi:{round(kx[0][0]*el+kx[1][0])}')
        print()
        print(f'Дисперсия {sum([(y[ind] - kx[0][0]*el+kx[1][0])**2 for ind, el in enumerate(x)])}')
        plt.plot(x1, y1)
        plt.scatter(x, y)
    else:
        return [x1, y1]

def ax2(path, flag = True):
    """Апроксимация Квадратичной функцией
    
    path - Путь к x, y
    flag - Влияет на вывод ответа
    Либо Просто точки,
    Либо Графики
    """
    x, y = csv(path)
    
    
    kx = solve([[sum([i**4 for i in x]),sum([i**3 for i in x]),sum([i**2 for i in x])],
                [sum([i**3 for i in x]),sum([i**2 for i in x]),sum([i**1 for i in x])],
                [sum([i**2 for i in x]),sum([i**1 for i in x]),len(x)]],
                [[sum([(x[i]**2)*y[i] for i in range(len(x))])],
                 [sum([x[i]*y[i] for i in range(len(x))])],
                 [sum([y[i] for i in range(len(x))])]])
    
    x1 = []
    y1 = []
    for i in range(int(min(x))*10, (int(max(x))+1)*10):
        x1.append(i/10)
        y1.append(kx[0][0]*(i/10)**2+kx[1][0]*i/10+kx[2][0])
    if flag:
        print(f'y = {kx[0][0]}x**2+{kx[1][0]}x + {kx[2][0]}')
        print()
        for ind, el in enumerate(x):
            print(f'x:{el} y:{y[ind]} fi:{kx[0][0]*(el)**2+kx[1][0]*el+kx[2][0]}')
        print()
        print(f'Дисперсия {sum([(y[ind] - kx[0][0]*(x[ind])**2+kx[1][0]*x[ind]+kx[2][0])**2 for ind, el in enumerate(x)])}')
        plt.plot(x1, y1)
        plt.scatter(x, y)
    else:
        return [x1, y1]

def norm_v2(path, flag = True):
    """Апроксимация Нормальным распределением
    
    path - Путь к x, y
    flag - Влияет на вывод ответа
    Либо Просто точки,
    Либо Графики"""
    
    x, y = reading_csv(path)
    X = []
    Y = []
    for ind, el in enumerate(x):
        X.append([1, el, el**2])
        Y.append([log(y[ind])])
    B = dot(dot(linalg.inv(dot(array(X).T,array(X))), array(X).T), array(Y))
    
    a = exp(B[0][0] - (B[1][0]**2)/(4*B[2][0]))
    b = - (1/(B[2][0]))
    c = - (B[1][0]/(B[2][0]*2))
    
    f = lambda x: a * exp(-((x - c)**2/b))
    
    x1 = []
    y1 = []
    for el in arange(min(x), max(x), 0.1):
        x1.append(el)
        y1.append(f(el))
    plt.plot(x1, y1, color = 'orange')
    plt.scatter(x, y)

def numpy_poli(path, flag):
    """Выдает точки через Нумпай Полифит
    Path - Путь к файлу
    return точки для построения """
    x, y = csv(path = path)
    
    x1 = []
    y1 = []
    formula = ''
    m = polyfit(x, y, 2)
    for ind, el in enumerate(m):
        formula += f'+{el}*x**{len(m)-ind-1}'
    for x_el in range((int(min(x)))*10, (int(max(x))+1)*10):
        x1.append(x_el/10)
        y1.append(eval(formula.replace("x", str(eval(f'{x_el}/10')))))
    return [x1, y1]
    
def scipy_interpol(path, flag):
    """Выдает точки через Нумпай Полифит
    Path - Путь к файлу
    return точки для построения """
    x, y = csv(path = path)
    from scipy import interpolate
    from numpy import arange
    import matplotlib.pyplot as plt
    f = interpolate.interp1d(x, y, kind = 'cubic')
    xnew = arange(min(x), max(x), 0.1)
    
    ynew = f(xnew)
    return [xnew, ynew]
    
def comparison(path):
    """Объединение всех функций интерполяции и Апроксимации
    path - путь к точкам"""
    x, y = csv(path = path)
    
    fig, axes = plt.subplots(2, 4)
    
    function_list = [[lagrange, scipy_interpol], [kx, ax2, numpy_poli]]
    for ind, i_a in enumerate(function_list):
        for i, func in enumerate(i_a):
#             print(func)
            m = func(path = path, flag = False)
            axes[ind][i].set_title(func.__name__)
            axes[ind][i].plot(m[0], m[1])
            axes[ind][i].scatter(x, y, color = 'orange')
#             print(func.__name__)
    m = newton(path, FoS = 'F', flag =False)
    axes[0][2].set_title('Newton F')
    axes[0][2].plot(m[0], m[1])
    axes[0][2].scatter(x, y, color = 'orange')
#     print('newton >')
    m = newton(path, FoS = 'S', flag =False)
    axes[0][3].set_title('Newton S')
    axes[0][3].plot(m[0], m[1])
    axes[0][3].scatter(x, y, color = 'orange')
#     print('newton <')
    m = al_aprr(path, 'c1 * E**(-((x-c2)**2)/(c3**2))', [c1, c2, c3], flag = False)
    axes[1][3].set_title('Нормальное')
    axes[1][3].plot(m[0], m[1])
    axes[1][3].scatter(x, y, color = 'orange')
    
    fig.set_figheight(10)
    fig.set_figwidth(16)