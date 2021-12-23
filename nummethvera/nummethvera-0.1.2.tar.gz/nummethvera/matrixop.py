import copy

def inp_matr():
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



def outp_matr(a):
    """
    Выводит на экран пользователя матрицу a.

    Parameters
    ----------
    a : [[float, float, ...],
         [float, float, ...],
         ...]
        Матрица, введенная пользователем

    """
    for i in range(len(a)): 
        print(f'{a[i]}')      



def transp(A):
    """
    Возвращает транспонированную исходную матрицу

    Parameters
    ----------
    A : [[float, float, ...],
         [float, float, ...],
         ...]
        Матрица, которую нужно транспонировать

    Returns
    -------
    list
        Транспонированная матрица

    """
    print('Транспонированная матрица:')
    return [[x[i] for x in A] for  i in range(len(A[0]))]



def summfunc(A,B):
    """
    Сложение двух матриц

    Parameters
    ----------
    A : [[float, float, ...],
         [float, float, ...],
         ...]
        Первая матрица, которую нужно сложить
    B : [[float, float, ...],
         [float, float, ...],
         ...]
        Вторая матрица, которую нужно сложить

    Raises
    ------
    ValueError
        Возникает при разных размерностях матриц.

    Returns
    -------
    summ : [[float, float, ...],
            [float, float, ...],
            ...]
        Матрица, которая является суммой матриц A и B.

    """
    n = len(A)
    m = len(A[0])
    n1 = len(B)
    m1 = len(B[0])
    if n != n1 or m != m1:
        raise ValueError('Разные размерности матриц, введите матрицу/ы заново')
    summ = []
    for i in range(n):
        summ.append([])
        for j in range(m):
            summ[i].append(A[i][j] + B[i][j])
    return summ



def subtfunc(A,B):
    """
    Вычитание одной матрицы из другой

    Parameters
    ----------
    A : [[float, float, ...],
         [float, float, ...],
         ...]
        Матрица, из которой будем вычитать
    B : [[float, float, ...],
         [float, float, ...],
         ...]
        Матрица, которую будем вычитать

    Raises
    ------
    ValueError
        Возникает при разных размерностях матриц.

    Returns
    -------
    subt : [[float, float, ...],
            [float, float, ...],
            ...]
        Матрица, которая является разностью матриц A и B

    """
    n = len(A)
    m = len(A[0])
    n1 = len(B)
    m1 = len(B[0])
    if n != n1 or m != m1:
        raise ValueError('Разные размерности матриц, введите матрицу/ы заново')
    subt = []
    for i in range(n):
        subt.append([])
        for j in range(m):
            subt[i].append(A[i][j] - B[i][j])
    return subt



def multnumfunc(num, A):
    """
    Умножение матрицы на число или список.

    Parameters
    ----------
    num : float
        Число, на которое нужно умножить матрицу
    A : [[float, float, ...],
         [float, float, ...],
         ...]
        Матрица, которую умножаем на число

    Raises
    ------
    ValueError
        Возникает, если первым элементов является матрица, а вторым - число.

    Returns
    -------
    mult : [[float, float, ...],
            [float, float, ...],
            ...]
        Матрица, которая является результатом умножения числа num на матрицу A.

    """
    if type(num) != type(1) and type(num) != type(1.1) or type(A) != type([]):
        raise ValueError('Первый элемент должен быть числом, а второй - матрицей')
    n = len(A)
    m = len(A[0])
    mult = []
    for i in range(n):
        mult.append([])
        for j in range(m):
            mult[i].append(A[i][j] * num)
    return mult



def multfunc(A,B):
    """
    Умножение двух матриц

    Parameters
    ----------
    A : [[float, float, ...],
         [float, float, ...],
         ...]
        Первая матрица, которую будем складывать
    B : [[float, float, ...],
         [float, float, ...],
         ...]
        Вторая матрица, которую будем складывать 

    Raises
    ------
    ValueError
        Возникает, когда кол-во строк матрицы A не совпадает с кол-вом столбцов матрицы B.

    Returns
    -------
    mult : [[float, float, ...],
            [float, float, ...],
            ...]
        Матрица, которая является произведением матриц A и B

    """
    n = len(A)
    m = len(B[0])
    t = len(A[0])
    l = len(B)
    if t != l:
        raise ValueError('Кол-во столбцов первой матрицы и кол-во строк второй должны совпадать. Попробуйте ввести матрицы еще раз!')
    mult = []
    for i in range(n):
        mult.append([])
        for j in range(m):
            s = 0
            for k in range(t):
                s += A[i][k] * B[k][j]
            mult[i].append(s)
    return mult



def process(func):
    """
    Выводит преобразованную в команды строку

    Parameters
    ----------
    func : str
        Строка с командами, введённая пользователем

    Returns
    -------
    func : str
        Преобразованная в команды строка

    """
    dicti = {'@': 'multfunc', '*': 'multnumfunc', '+': 'summfunc', '-': 'subtfunc'}
    func = func.replace('(', ' ( ').replace(')', ' ) ')
    func = func.split()
    while '(' in func:
        i1 = func.index('(')
        count = 1
        for r in range(i1 + 1, len(func)):
            if func[r] == '(':
                count += 1
            elif func[r] == ')':
                count -= 1
            if count == 0:
                i2 = r
                break
        part1 = func[:i1]
        part2 = func[i2 + 1:]
        res = process(' '.join(func[i1 + 1:i2]))
        func = part1 + res + part2
    for _ in range(len(func)):
        i = '*'
        if i in func:
            index = func.index(i)
            l1 = func[index-1]
            l2 = func[index]
            l3 = func[index+1]
            out = dicti[l2] + '(' + l1 + ',' + l3 + ')'
            func[index] = out
            func.pop(index+1)
            func.pop(index-1)
                
    for _ in range(len(func)):
        i = '@'
        if i in func:
            index = func.index(i)
            l1 = func[index-1]
            l2 = func[index]
            l3 = func[index+1]
            out = dicti[l2] + '(' + l1 + ',' + l3 + ')'
            func[index] = out
            func.pop(index+1)
            func.pop(index-1)
            
    for _ in range(len(func)):
        for i in ["+", "-"]:
            if i in func:
                index = func.index(i)
                l1 = func[index-1]
                l2 = func[index]
                l3 = func[index+1]
                out = dicti[l2] + '(' + l1 + ',' + l3 + ')'
                func[index] = out
                func.pop(index+1)
                func.pop(index-1)
    return func



def f(func):
    """
    Функция выполняет все математические операции, введённые пользователем.

    Parameters
    ----------
    func : str
        Преобразованная в командры строка

    Returns
    -------
    [[float, float, ...],
            [float, float, ...],
            ...]
        Матрица, которая является резульатом выполнения всех операций, введённых пользователем.

    """
    func = ''.join(process(func))
    print(func)
    return eval(func)



def det(a):
    """
    Функция вычисляет определитель матрицы.

    Parameters
    ----------
    a : [[float, float, ...],
         [float, float, ...],
         ...]
        Матрица, введенная пользователем

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


def calculation(func):
    """
    Функция, в которой выполняются нужные математические операции

    Parameters
    ----------
    func : str
        Функция преобразования матриц, введённая пользователем

    Returns
    -------
    [[float, float, ...],
            [float, float, ...],
            ...]
        Матрица, которая является результатом вычисления

    """
    while True:
        func = input('Введите преобразование: ')
        if func.count('(') != func.count(')'):
            print('Кол-во открывающих скобок должно быть равно кол-ву закрывающих скобок')
        else:
            break
    temp = func.replace('+', ' ').replace('-', ' ').replace('*', ' ').replace('@', ' ').replace(')', ' ').replace('(', ' ')
    temp = temp.split()
    temp = sorted(list(set(temp)))
    print(temp)
    for s in temp:
        if s.isalpha():
            print(f'Введите матрицу {s}')
            exec(f'{s} = inp_matr()')
            eval(f"outp_matr({s})")
    return f(func)




