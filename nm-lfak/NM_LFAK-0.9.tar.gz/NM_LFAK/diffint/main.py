def diff_by_Jay(f, left, right, num_of_dots, dx):
    """ Функция выводит графики производных через формулу и стандартные методы
    
    f - Функция
    left - левая граница
    right - правая граница
    num_of_dots - количество точек в интервале 
    dx - ша с которым мы ищем производную
    
    Пример:
    diff_by_Jay('1/x**2', -2, 2, 60, 0.1)"""
    
    # ==========Задали функции==============
    
    x, y = sm.symbols('x y')
    
    func = sm.parse_expr(f)
    
    func_d = sm.diff(func)
    
    
    # =====Формула рассчета производной=====
    
    func_d_hands = lambda x1, dx: (func.evalf(subs={x:x1 + dx}) - func.evalf(subs={x:x1 - dx}))/(2*dx)
    
    # =======Определение интервала==========
    left_b = eval(str(left))
    right_b = eval(str(right))
    num = int(eval(str(num_of_dots))//1)
                                              
    x1 = list(linspace(left_b, right_b, num = num))
    
                                              
    # ==========Подсчет значений============
                                              
    y_f = []
    y_df1 = []
    y_df2 = []
    helpi = [] 
    for i in x1:
        try:
            a = func.evalf(subs={x:i})
            b = func_d.evalf(subs={x:i})
            c = func_d_hands(i, dx)
            y_f.append(a)
            y_df1.append(b)
            y_df2.append(c)
        except:
            helpi.append(i)
    
    for h in helpi:
        x1.remove(h)
    
    # ========Создание ДатаФрейма============
    
    df = pd.DataFrame({'x': x1, "f(x)": y_f, "f'(x)s": y_df1, "f'(x)h": y_df2})
    
    # ==========Построение графика============
    fig, axes = plt.subplots(1, 3)

    
    axes[0].plot(df['x'],df['f(x)'])
    axes[1].plot(df['x'],df["f'(x)s"])
    axes[2].scatter(df['x'],df["f'(x)h"],marker ='.',linewidths=0.5)


    axes[0].set_title("f(x)",
                    loc = 'center',
                    pad = 10,
                    fontsize = 20)    

    axes[1].set_title("f'(x)s",
                    loc = 'center',     
                    pad = 10,
                    fontsize = 20)

    axes[2].set_title("f'(x)h",
                    loc = 'center',
                    pad = 10,
                    fontsize = 20)


    for ax in axes:
        ax.grid(axis = 'both')

    fig.suptitle('Графики',
                    fontsize = 20,
                    y = 1.1)

    fig.set_figheight(4)
    fig.set_figwidth(16)

    plt.show()
    
    print(df)
    
    
def integr_by_Jay(f, left, right, step):
    
    """Функция считает площадь под графиком на интервале
    f - Функция 
    left - левая граница
    right - правая граница
    step - шаг для метода трапеций
    
    Пример 
    integr_by_Jay('x', 2, 20, 0.6)"""
    # ==========Задали функции==============
    
    x, y = sm.symbols('x y')
    
    func = sm.parse_expr(f)
    
    func_d = sm.diff(func)
    
    left_b = eval(str(left))
    right_b = eval(str(right))
    
    
    
    # constconstconstconstconstconstconstconst
    
    min_step = step
    
    left_tr = left
    der_l = func_d.evalf(subs={x:left_tr})
    
    right_tr = left_tr + min_step
    
    
    square = 0
    list_of_tr = []
    
    # constconstconstconstconstconstconstconst
    
    
    
    while not(right_tr >= right_b):
        
#         der_r = func_d.evalf(subs={x:right_tr})
        
        if True:
            
            list_of_tr.append([left_tr,func.evalf(subs={x:left_tr}),right_tr,func.evalf(subs={x:right_tr})])
            
            left_tr = right_tr
            right_tr = left_tr + min_step
#             der_l =func_d.evalf(subs={x:left_tr})
            
        else:
            right_tr += min_step
            if right_tr >= right_b:
                list_of_tr.append([left_tr,func.evalf(subs={x:left_tr}),right_tr,func.evalf(subs={x:right_tr})])
         
    
#     =========== Построение графиков =============
    x_spl = list(linspace(left_b, right_b, int((abs(left_b-right_b)*100)//1)))
    y = []
    helpi = [] 
    for i in x_spl:
        try:
            a = func.evalf(subs={x:i})
            y.append(a)
        except:
            helpi.append(i)
    
    for h in helpi:
        x_spl.remove(h)
    
    
    fig, ax = plt.subplots()
    
    ax.plot(x_spl, y)
    
    for s in list_of_tr:
        ax.plot([s[0],s[0],s[2],s[2]],[0,s[1], s[3],0])
        square += (abs((s[0]-s[2]))*(s[1]+s[3]))/2
    
    print('S = ', square) 
    
def S(f, left, right):
    
    """Вспомогательная функция, которая ищет площадь под графиком
    
    f - Функция
    left - Левая граница
    right - Правая граница"""
    
    # ==========Задали функции==============
    
    x, y = sm.symbols('x y')
    
    func = sm.parse_expr(f)
    
    func_d = sm.diff(func)
    
    left_b = eval(str(left))
    right_b = eval(str(right))
    
    
    
    # constconstconstconstconstconstconstconst
    
    min_step = 0.001
    
    left_tr = left
    der_l = func_d.evalf(subs={x:left_tr})
    
    right_tr = left_tr + min_step
    
    
    square = 0
    list_of_tr = []
    
    # constconstconstconstconstconstconstconst
    
    
    
    while not(right_tr >= right_b):
        
        der_r = func_d.evalf(subs={x:right_tr})
        
        if abs(der_l - der_r) >= 0.001:
            
            list_of_tr.append([left_tr,func.evalf(subs={x:left_tr}),right_tr,func.evalf(subs={x:right_tr})])
            
            left_tr = right_tr
            right_tr = left_tr + min_step
            der_l =func_d.evalf(subs={x:left_tr})
            
        else:
            right_tr += min_step
            if right_tr >= right_b:
                list_of_tr.append([left_tr,func.evalf(subs={x:left_tr}),right_tr,func.evalf(subs={x:right_tr})])
         
    for s in list_of_tr:

        square += (abs((s[0]-s[2]))*(s[1]+s[3]))/2
    
    return eval(str(square))
    
def antiderivative_by_Jay(f, left, right):
   
    """Построение графика интеграла
    
    f - Функция
    left - Левая граница
    right - Правая граница
    
    Пример
    antiderivative_by_Jay('x**2',-5, 5)"""
        
    x, y = sm.symbols('x y')
    
    func = sm.parse_expr(f)
    step = 0.1
    left_b = eval(str(left))
    left_h = left_b + step 
    right_b = eval(str(right))

    x1 = []
    y1 = []
    
    y1.append(S(f, left_b, left_h))

    x1.append(left_h)
    
    while not(left_h >= right_b):
        left_h += step

        y1.append(y1[-1] + S(f,x1[-1], left_h))
        x1.append(left_h)
    
    plt.scatter(x1,y1,marker ='.',linewidths=0.5)

from numpy import *
import pandas as pd
import sympy as sm
import matplotlib.pyplot as plt