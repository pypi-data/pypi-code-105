from math import *
import mpmath 

def input_func():
    """
    Возвращает введенную функцию и её параметры.

    Returns
    -------
    func : str
        Исходная функция
    a : float
        Левая граница интервала
    b : float
        Правая граница интервала
    h : float
        Шаг или точность

    """
    
    mpmath.mp.dps = 64
    func = input('Введите функцию\n')
    
    def f(x):
        z = eval(func)
        return z
    
    while True:
        try:
            f(1)
        except Exception as e:
            print(e)
            print('Ошибка в функции, введите функцию еще раз\n')
            func = input()
        else:
            break
    
    while True:
        try:
            a = float(input('Введите левую границу интервала\n'))
        except:
            print('Введите число')
        else:
            break
    
    while True:
        try:
            b = float(input('Введите правую границу интервала\n'))
        except:
            print('Введите число')
        else:
            break
    
    ans = input('Вы хотите задать шаг или точность? (1 - шаг; 2 - точность)\n')
    flag = True
    while flag: 
        if ans == '1':
            while True:
                try:
                    h = float(input('Введите шаг\n'))
                except:
                    print('Введите число, например 0.001')
                else:
                    break
            flag = not flag
        elif ans == '2':
            while True:
                try:
                    h = float(input('Введите точность\n'))**0.5
                except:
                    print('Введите число, например 0.001')
                else:
                    break
            flag = not flag
        else:
            print('Введите "1" или "2"')
            ans = input()
            
    if b < a:
        a, b = b, a
        
    return func, a, b, h



def diff(a, b, h, func):
    """
    Дифференцирование по формуле

    Parameters
    ----------
    a : float
        Левая граница интервала
    b : float
        Правая граница интервала
    h : float
        Шаг или точность
    func : str
        Исходная функция

    Returns
    -------
    xspis : [float, float, ...]
        Список значений координат x
    yspis : [float, float, ...]
        Список значений координат y
    ydiffspis : [float, float, ...]
        Список значений производной функции 

    """
    ydiffspis = []
    yspis = []
    xspis = []
    banspis = []
    
    def f(x):
        z = eval(func)
        return z
    
    c = int(1/h)
    for i in range(int(a*c),int(b*c)+1,round(h*c)):
        try:
            diff = (f((i/c)+h)-f((i/c)-h))/(2*h)
            yspis.append(f(i/c))
            xspis.append(i/c)
            ydiffspis.append(diff)
        except:
            print(f'Точка разрыва в координате х = {i/c}')
            banspis.append(i/c)
            continue
    return xspis, yspis, ydiffspis



def integ(a, b, h, func):
    """
    Интегрирование по формуле

    Parameters
    ----------
    a : float
        Левая граница интервала
    b : float
        Правая граница интервала
    h : float
        Шаг или точность
    func : str
        Исходная функция

    Returns
    -------
    S1 : float
        Значение определенного интеграла
    slist : [float, float, ...]
        История изменений значения определенного интеграла.

    """
    
    ylist1 = []
    slist = []
    xlist1 = []
    banlist = []
    
    def f(x):
        z = eval(func)
        return z

    S1 = 0
    c = int(1/h)
    for i in range(int(a*c),int(b*c),round(h*c)):
        try:
            S1 = S1 + ((f(i/c)+f(i/c+h))/2)*h
            xlist1.append(i/c)
            ylist1.append(f(i/c))
            slist.append(S1)
        except:
            print('Деление на 0')
            banlist.append(i/c)
            
    return S1, slist