from numpy import arange, e, sin, cos
import matplotlib.pyplot as plt
from pandas import DataFrame

def Eiler_Koshi(functions, start, limits):
    
    '''
    Входные данные:
    Функции - [func1, func2 ...],
    Нач усл - [y1, y2 ...],
    Границы - [left, right, step]   
    '''
    
    
    
    dict_of_func = {}
    for func in functions:
        dict_of_func[func[:(func.find("'"))]] = func[(func.find('=')+1):].replace(' ','')

    x_plot = arange(limits[0],limits[1],limits[2])
    

    k = 0
    formats_i = ''
    formats_i1 = ''
    for key, val in dict_of_func.items():
        exec(f'{key}_i =  {start[k]}')
        exec(f'{key}_i1 = {start[k]}')
        exec(f'{key}_plot = []')
        formats_i += f'.replace("{key}", str({key}_i)).replace("x",str(x))'
        formats_i1 += f'.replace("{key}", str({key}_i1)).replace("x",str(x+limits[2]))'
        k += 1

        
    for x in x_plot:
        
        for key, val in dict_of_func.items():
            exec(f'{key}_i = {key}_i1')
            
        for key, val in dict_of_func.items():
            exec(f'{key}_i1 = float(eval(str({key}_i)+"+"+str({limits[2]})+"*"+str(eval("{val}"{formats_i}))))')
                
        for key, val in dict_of_func.items():
            exec(f'{key}_i1 = float(eval(str({key}_i))){"+"}{limits[2]}/2{"*("}float(eval("{val}"{formats_i})){"+"}float(eval("{val}"{formats_i1})){")"}')
            
        for key, val in dict_of_func.items():
            exec(f'{key}_plot.append({key}_i1)')
    
    dict_for_df = {'x': x_plot}
    for key, val in dict_of_func.items():  
        exec(f'dict_for_df["{key}"] = {key}_plot')
        
    return DataFrame(dict_for_df)
def Runge_Kutta(functions, start, limits):
    
    '''
    Входные данные:
    Функции - [func1, func2 ...],
    Нач усл - [y1, y2 ...],
    Границы - [left, right, step]   
    '''
    
    
    
    dict_of_func = {}
    for func in functions:
        dict_of_func[func[:(func.find("'"))]] = func[(func.find('=')+1):].replace(' ','')

    x_plot = arange(limits[0],limits[1] + limits[2],limits[2])
    

    k = 0
    formats_i_1 = ''
    formats_i_2 = ''
    formats_i_3 = ''
    formats_i_4 = ''
    
    for key, val in dict_of_func.items():
        exec(f'{key}_i =  {start[k]}')
        exec(f'{key}_plot = []')
        formats_i_1 += f'.replace("{key}", str({key}_i)).replace("x",str(x))'
        formats_i_2 += f'.replace("{key}", str({key}_i + {key}_1/2)).replace("x",str(x + limits[2]/2))'
        formats_i_3 += f'.replace("{key}", str({key}_i + {key}_2/2)).replace("x",str(x + limits[2]/2))'
        formats_i_4 += f'.replace("{key}", str({key}_i + {key}_3/2)).replace("x",str(x + limits[2]/2))'
        k += 1

        
    for x in x_plot:
         
        for key, val in dict_of_func.items():
            exec(f'{key}_plot.append({key}_i)')
            
        for key, val in dict_of_func.items():
            exec(f'{key}_1 = {limits[2]} * float(eval("{val}"{formats_i_1}))')
            
        for key, val in dict_of_func.items():
            exec(f'{key}_2 = {limits[2]} * float(eval("{val}"{formats_i_2}))')
                
        for key, val in dict_of_func.items():
            exec(f'{key}_3 = {limits[2]} * float(eval("{val}"{formats_i_3}))')
            
        for key, val in dict_of_func.items():
            exec(f'{key}_4 = {limits[2]} * float(eval("{val}"{formats_i_4}))')
    
        for key, val in dict_of_func.items():
            exec(f'{key}_i = {key}_i + (1/6)*({key}_1+2*{key}_2+2*{key}_3+{key}_4)')
            
        
                 
    dict_for_df = {'x': x_plot}
    for key, val in dict_of_func.items():  
        exec(f'dict_for_df["{key}"] = {key}_plot')
        
    return DataFrame(dict_for_df)
    
def analysis(df):
    """Просто отправьте в эту функци ответ от (Runge Kutta например...)"""
    
    
    cols = df.columns.tolist()
    
    for element in cols[1:]:
        plt.scatter(df[cols[0]], df[element], label = f'{element}({cols[0]})')
        plt.legend()
        plt.show()
        newton(list(df[cols[0]]),list(df[element]))
        ax2(list(df[cols[0]]),list(df[element]))


def newton_table(x, y):
    import numpy as np
    table = [[0 for j in range(len(x))] for i in range(len(x)+1)]
    table[0], table[1] = x, y 
    for ind, el in enumerate(table[2:]):
        for i in range(len(el)-ind-1):
            table[ind+2][i] = -(table[ind+1][i] - table[ind+1][i+1])
    table = np.array(table).T
    return table

def factor(n):
    r = 1
    for i in range(1,n+1):
        r = r*i   
    return r

def check_step(x):
    s = x[1] - x[0]
    return s

def first_newton_F(x, y, table):
    from sympy import simplify, expand, Symbol
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

def second_newton_F(x, y, table):
    
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
def newton(X, Y, header = False, delimiter = ',', flag = True):
    import matplotlib.pyplot as plt
    from numpy import arange
    print('----------Интерполяция методом Ньютона-----------')
    
    x, y = X, Y
    
    F = first_newton_F(x, y, newton_table(x, y))
    
    x1 = []
    y1 = []

    for i in arange(min(x), max(x), 0.01):
        x1.append(i)
        y1.append(eval(F.replace("x", str(i))))
#     print(F)
    plt.plot(x1,y1)
    plt.show()
    
        
        
    
def ax2(X, Y, flag = True):
    x, y = X, Y
    from numpy import arange
    from scipy.linalg import solve
    import matplotlib.pyplot as plt
    
    kx = solve([[sum([i**4 for i in x]),sum([i**3 for i in x]),sum([i**2 for i in x])],
                [sum([i**3 for i in x]),sum([i**2 for i in x]),sum([i**1 for i in x])],
                [sum([i**2 for i in x]),sum([i**1 for i in x]),len(x)]],
                [[sum([(x[i]**2)*y[i] for i in range(len(x))])],
                 [sum([x[i]*y[i] for i in range(len(x))])],
                 [sum([y[i] for i in range(len(x))])]])
    x1 = []
    y1 = []
    for i in arange(min(x), max(x), 0.01):
        x1.append(i)
        y1.append(kx[0][0]*(i)**2+kx[1][0]*i+kx[2][0])
    print('----------------Апроксимация----------------')
    print(f'y = {kx[0][0]}x**2+{kx[1][0]}x + {kx[2][0]}')
    print()
    plt.plot(x1, y1)
    plt.scatter(x, y, color ='red')
    plt.show()

