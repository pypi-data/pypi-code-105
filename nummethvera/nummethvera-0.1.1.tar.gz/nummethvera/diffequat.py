from sympy import *
import numpy as np
import matplotlib.pyplot as plt

def draw_plot(values, label, three_d=False):
    """
    Функция отрисовки графика функции по её передаваемым значениям

    Parameters
    ----------
    values : [[float, float, ...],
              [float, float, ...],
              ...]
        Список из списков групп значений x, y, y', y'' и тд.
    label : str
        Подпись функции на графике.
    three_d : bool, optional
        Отрисовка графика в 3D. 
        По умолчанию False.

    Raises
    ------
    ValueError
        Возникает при попытке нарисовать 3D график используя только 2 переменные.
        
    """
    if not three_d or len(values) < 3:
        if three_d:
            raise ValueError('Предупреждение, вы не можете построить 3D график используя только две переменные')
        try:
            x_list = values[:, 1]
            y_list = values[:, 2]
        except:
            x_list = values[0]
            y_list = values[1]
        plt.plot(x_list, y_list, label=label)
        plt.legend()
        plt.show()
    else:
        try:
            x_list = values[:, 1]
            y_list = values[:, 2]
            z_list = values[:, 3]
        except:
            x_list = values[0]
            y_list = values[1]
            z_list = values[2]
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.plot(x_list, y_list, z_list, label=label)
        ax.legend(loc='upper left')
        plt.show()
        

def draw_plots(values, labels, colors=[], three_d=False):
    """
    

    Parameters
    ----------
    values : [[[float, float, ...],
              [float, float, ...],
              ...],
              [[float, float, ...],
              [float, float, ...],
              ...], ...]
        Список из нескольких списков из групп значений x, y, y', y'' и тд. (Несколько графиков)
    labels : [str, str, ...]
        Список подписей функций на графике.
    colors : [str, str, ...], optional
        Список цветов отрисовки графиков. 
        По умолчанию [].
    three_d : bool, optional
        Отрисовка графика в 3D. 
        По умолчанию False.

    """
    
    if not three_d:
        for i in range(len(values)):
            try:
                x_list = values[i][:, 1]
                y_list = values[i][:, 2]
            except:
                x_list = values[i][0]
                y_list = values[i][1]
            if colors:
                plt.plot(x_list, y_list, colors[i], label=labels[i])
            else:
                plt.plot(x_list, y_list, label=labels[i])
        plt.legend()
        plt.show()
    else:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        for i in range(len(values)):   
            try:
                x_list = values[i][:, 1]
                y_list = values[i][:, 2]
                z_list = values[i][:, 3]
            except:
                x_list = values[i][0]
                y_list = values[i][1]
                z_list = values[i][2]
            if colors:
                ax.plot(x_list, y_list, z_list, color=colors[i], label=labels[i])
            else:
                ax.plot(x_list, y_list, z_list, label=labels[i])                                                 
        ax.legend(loc='upper left')
        plt.show()



def input_expression():
    """
    Возвращает введённую функцию\функции 
    
    Returns
    -------
    expressions : optional - (exp1, exp2) or (exp, )
        Кортеж из функции\системы двух функции.
    n : int
        Колв-во  введённых функций.

    """
    
    n = int(input('Введите кол-во уравнений, которые хотите задать (1|2)\n ->'))
    if n == 1:
        expression = input('Введите уравнение\n ->')
        return (expression, ), 1
    exp1 = input("Введите первое уравнение\n ->y'=")
    exp2 = input("Введите второе уравнение\n ->z'=")
    return (exp1, exp2), 2  

def lambda_func(string, variables):
    """
    Генерирует на основании введённого уравнения - его представление в функциях

    Parameters
    ----------
    string : srt
        Введённое уравнение.
    variables : [str, str, ...]
        Список переменных, встречающихся в уравнении.

    Returns
    -------
    func: function
        Лямбда-функция, основанная на введённом уравнении.

    """
    var = []
    for v in variables:
        exec(f'{v} = Symbol("{v}")')
        eval(f'var.append({v})')
    expr = eval(string.replace('^', '**'))
    return lambdify(var, expr)
    
def parse_string(string):
    """
    Парсер, приводящий любое уравнение к виду y'(n) = x + y' + y'' + y''' + ... + y'(n-1)

    Parameters
    ----------
    string : str
        Введённое уравнение.

    Returns
    -------
    exp : str
        Преобразованное уравнение.
    max_val : int
        Степень диф. уравнения.
    variables : [str, str, ...]
        Список участвующих в уравнении переменных.

    """
    
    string = string.replace(' ', '')
    expression = []
    variable = ''
    for i in range(len(string)):
        variable += string[i]
        if i == len(string) - 1:
            expression.append(variable)
            variable = ''
        elif not (string[i + 1] in "'^" or string[i + 1].isalpha() or string[i + 1].isdigit()) or string[i] in '=+*/-':
            expression.append(variable)
            variable = ''
    max_ind = 0
    max_val = -1
    for var in expression:
        if var.count("'") > max_val:
            max_val = var.count("'")
            max_ind = expression.index(var)
    val = expression[max_ind]
    eq = expression.index('=')
    if eq < max_ind:
        expression = expression[eq + 1:] + ['='] + expression[:eq]
    eq = expression.index('=')
    left = expression[:eq]
    if left[0] not in '+-' and ((val in left) == (len(left) > 2)) or len(left) == 1:
        left = ['+'] + left
    right = expression[eq + 1:]
    if right[0] not in '+-' and ((val in right) == (len(right) > 2)) or len(left) == 1:
        right = ['+'] + right
    new_ind = left.index(val)
    sign = left[new_ind - 1]
    left.pop(new_ind)
    left.pop(new_ind - 1)
    if sign == '+' and len(left) != 0:
        expression = right + ['-', '(']  + left + [')']
    elif sign == '+':
        expression = right
    elif sign == '-' and len(right) != 0:
        expression = left + ['-', '(']  + right + [')']
    else:
        expression = left
    if expression[0] == '+':
        expression.pop(0)
    variables = []
    for v in expression:
        temp = []
        for s in v:
            temp.append(s.isalpha())
        if sum(temp):
            new_temp = []
            for s in v:
                if s.isalpha() or s == "'":
                    new_temp.append(s)
            variables.append(''.join(new_temp))
    variables = sorted(variables)
    variables = sorted(variables, key=lambda x: len(x))
    print(f"Функция : {' '.join(expression)}\nСтепень дифф. уравнения: {max_val}")
    return ' '.join(expression), max_val, variables


def eyler_cauchy(f, power, var, n=10000):
    """
    Решение диф. уравнение методом Эйлера-Коши

    Parameters
    ----------
    f : str
        Введённая функция.
    power : int
        Степень диф. уравнения.
    var : [str, str, ...]
        Список переменных.
    n : int, optional
        Кол-во получаемых значений. 
        По умолчанию 10000.

    Returns
    -------
    result : [[float, float, ...],
              [float, float, ...],
              ...]
        Список из списков групп значений x, y, y', y'' и тд.

    """
    
    for i in range(len(var)):
        if "'" in var[i]:
            var[i] = "y" + str(var[i].count("'") - 1)
    for v in var[::-1]:
        if v[-1].isdigit():
            f = f.replace('y' + "'" * (int(v[-1]) + 1), v)
            
    func = lambda_func(f, var)
    values_dict = {}
    for i in range(len(var)):
        values_dict[(i, var[i])] = [float(input(f'Введите начальные условия ({var[i]}_0)'))]
    
    a = float(input('Введите начальные условия (a)'))
    b = float(input('Введите начальные условия (b)'))
    h = (b-a)/n

    for i in range(n):
        values_i = []
        values_i1 = []
        for v in values_dict.keys():
            if v[0] == 0:
                values_dict[v].append(values_dict[v][i] + h)
                values_i.append(values_dict[v][i])
                values_i1.append(values_dict[v][i + 1])
            elif v[0] != len(values_dict.keys()) - 1:
                values_dict[v].append(values_dict[v][i] + h * values_dict[(v[0] + 1, var[v[0] + 1])][i])
                values_i.append(values_dict[v][i])
                values_i1.append(values_dict[v][i + 1])
            else:
                values_i.append(values_dict[v][i])
                values_i1.append(values_dict[v][i] + h * func(*values_i))
                values_dict[v].append(values_dict[v][i] + h / 2 * (func(*values_i) + func(*values_i1)))
    result = []
    for i in range(n + 1):
        result.append([])
        result[i].append(i)
        for v in values_dict.keys():
            result[i].append(values_dict[v][i])
        result[i].append(func(*result[i][1:]))
    return np.array(result)

def runge_kutti(f, power, var, n=10000):
    """
    Решение диф. уравнение методом Рунге-Кутти

    Parameters
    ----------
    f : str
        Введённая функция.
    power : int
        Степень диф. уравнения.
    var : [str, str, ...]
        Список переменных.
    n : int, optional
        Кол-во получаемых значений. 
        По умолчанию 10000.

    Returns
    -------
    result : [[float, float, ...],
              [float, float, ...],
              ...]
        Список из списков групп значений x, y, y', y'' и тд.

    """
    for i in range(len(var)):
        if "'" in var[i]:
            var[i] = "y" + str(var[i].count("'") - 1)
    for v in var[::-1]:
        if v[-1].isdigit():
            f = f.replace('y' + "'" * (int(v[-1]) + 1), v)
    func = lambda_func(f, var)
    values_dict = {}
    for i in range(len(var)):
        values_dict[(i, var[i])] = [float(input(f'Введите начальные условия ({var[i]}_0)'))]
    
    a = float(input('Введите начальные условия (a)'))
    b = float(input('Введите начальные условия (b)'))
    h = (b-a)/n
    
    koefs = np.zeros((len(var), 4))
    koefs[0] = np.array([0, h, h, h])
    funcs = {}
    variables = []
    for v in var:
        exec(f'{v} = Symbol("{v}")')
        eval(f'variables.append({v})')
        
    for v in values_dict.keys():
        if v[0] != 0 and v[0] != len(values_dict.keys()) - 1:
            funcs[v[0]] = lambdify(variables, var[v[0] + 1])
        elif v[0] == len(values_dict.keys()) - 1:
            funcs[v[0]] = func
    for i in range(n):
        values_dict[(0, 'x')].append(values_dict[(0, 'x')][i] + h)
        values_i = []
        for v1 in values_dict.keys():
            values_i.append(values_dict[v1][i])
        values_i = np.array(values_i)
        for j in range(1, len(values_i)):
            koefs[j][0] = h * funcs[j](*values_i)
        for j in range(1, len(values_i)):
            koefs[j][1] = h * funcs[j](*(values_i + koefs[:, 0]/2))
        for j in range(1, len(values_i)):
            koefs[j][2] = h * funcs[j](*(values_i + koefs[:, 1]/2))
        for j in range(1, len(values_i)):
            koefs[j][3] = h * funcs[j](*(values_i + koefs[:, 2]))
        
        for v in values_dict.keys():
            if v[0] != 0:
                values_dict[v].append(values_dict[v][i] + 1/6*(koefs[v[0]][0] + 2 * koefs[v[0]][1] + 2 * koefs[v[0]][2] + koefs[v[0]][3]))
        
    result = []
    for i in range(n + 1):
        result.append([])
        result[i].append(i)
        for v in values_dict.keys():
            result[i].append(values_dict[v][i])
        result[i].append(func(*result[i][1:]))
    return np.array(result)

def eyler_cauchy_system(expressions, var=['x', 'y', 'z'], n=1000):
    """
    Решение системы из двух диф. уравнений методом Эйлера-Коши

    Parameters
    ----------
    expressions : [str, str]
        Список из двух введённых функций.
    var : [str, str, str], optional
        Список переменных.
        По умолчанию ['x', 'y', 'z']
    n : int, optional
        Кол-во получаемых значений. 
        По умолчанию 10000.

    Returns
    -------
    result : [[float, float, ...],
              [float, float, ...],
              ...]
        Список из списков групп значений x, y, y', y'' и тд.

    """
    funcs = {'y': lambda x, y, z: eval(expressions[0].replace('^', '**')),
             'z': lambda x, y, z: eval(expressions[0].replace('^', '**'))}
    x0 = float(input(f'Введите начальные условия (x0)\n ->'))
    y0 = float(input(f'Введите начальные условия (y0)\n ->'))
    z0 = float(input(f'Введите начальные условия (z0)\n ->'))
    a = float(input('Введите начальные условия (a)'))
    b = float(input('Введите начальные условия (b)'))
    h = (b-a)/n
    values_dict = {'x': [x0],
                   'y': [y0],
                   'z': [z0]}
    
    for i in range(n):
        values_dict['x'].append(values_dict['x'][i] + h)
        values_i = []
        for v1 in values_dict.keys():
            values_i.append(values_dict[v1][i])
        yw1, zw1 = values_dict['y'][i] + h * funcs['y'](*values_i),\
                   values_dict['z'][i] + h * funcs['z'](*values_i)
        values_i1 = [values_dict['x'][i + 1], yw1, zw1]
        values_dict['y'].append(values_dict['y'][i] + h / 2 * (funcs['y'](*values_i) + funcs['y'](*values_i1)))
        values_dict['z'].append(values_dict['z'][i] + h / 2 * (funcs['z'](*values_i) + funcs['z'](*values_i1)))
    
    result = []
    for i in range(n + 1):
        result.append([])
        result[i].append(i)
        for v in values_dict.keys():
            result[i].append(values_dict[v][i])
    return np.array(result)

def runge_kutti_system(expressions, var=['x', 'y', 'z'], n=1000):
    """
    Решение системы из двух диф. уравнений методом Рунге-Кутти

    Parameters
    ----------
    expressions : [str, str]
        Список из двух введённых функций.
    var : [str, str, str], optional
        Список переменных.
        По умолчанию ['x', 'y', 'z']
    n : int, optional
        Кол-во получаемых значений. 
        По умолчанию 10000.

    Returns
    -------
    result : [[float, float, ...],
              [float, float, ...],
              ...]
        Список из списков групп значений x, y, y', y'' и тд.

    """
    funcs = {'y': lambda x, y, z: eval(expressions[0].replace('^', '**')),
             'z': lambda x, y, z: eval(expressions[0].replace('^', '**'))}
    x0 = float(input(f'Введите начальные условия (x0)\n ->'))
    y0 = float(input(f'Введите начальные условия (y0)\n ->'))
    z0 = float(input(f'Введите начальные условия (z0)\n ->'))
    a = float(input('Введите начальные условия (a)'))
    b = float(input('Введите начальные условия (b)'))
    h = (b-a)/n
    values_dict = {'x': [x0],
                   'y': [y0],
                   'z': [z0]}
    
    for i in range(n):
        values_i = []
        for v1 in values_dict.keys():
            values_i.append(values_dict[v1][i])
        values_i = np.array(values_i)
        k1 = h * funcs['y'](*values_i)
        l1 = h * funcs['z'](*values_i)
        k2 = h * funcs['y'](*(values_i + np.array([h/2, k1/2, l1/2])))
        l2 = h * funcs['z'](*(values_i + np.array([h/2, k1/2, l1/2])))
        k3 = h * funcs['y'](*(values_i + np.array([h/2, k2/2, l2/2])))
        l3 = h * funcs['z'](*(values_i + np.array([h/2, k2/2, l2/2])))
        k4 = h * funcs['y'](*(values_i + np.array([h, k3, l3])))
        l4 = h * funcs['z'](*(values_i + np.array([h, k3, l3])))
        
        values_dict['x'].append(values_dict['x'][i] + h)
        values_dict['y'].append(values_dict['y'][i] + 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4))
        values_dict['z'].append(values_dict['z'][i] + 1 / 6 * (l1 + 2 * l2 + 2 * l3 + l4))
    
    result = []
    for i in range(n + 1):
        result.append([])
        result[i].append(i)
        for v in values_dict.keys():
            result[i].append(values_dict[v][i])
    return np.array(result)
    
def solve_expressions(expressions, function):
    """
    Решает диф. уравнение или систему диф. уравнение

    Parameters
    ----------
    expressions : optional (str, ) or (str1, str2)
        Введённые диф. уравнения.
    function : function
        Метод для решения диф. уравнений.

    Returns
    -------
    result : [[float, float, ...],
              [float, float, ...],
              ...]
        Список из списков групп значений x, y, y', y'' и тд.

    """
    if len(expressions) == 1:
        f, power, v = parse_string(expressions[0])
        res = function(f, power, v, n=100)
        return res
    return function(expressions)
    