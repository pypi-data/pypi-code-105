import csv 
import random
import numpy as np
import math
import matplotlib.pyplot as plt
from pylab import rcParams
from scipy.optimize import curve_fit 



def interpol():
    """
    FUNCTIONS:
        interpop.interpol()-основная работа программы
        находить интерполцию и аппроксимацию функции
    Входные данные:
        Выбор способа ввода 
        Кол-во значений
        Интервал значений
    Выходные данные:
        Данные подгонки полинома Тригонометрия
        Данные подгонки полинома Лагранж
        Данные подгонки полинома Гаусса
        Данные подгонки полинома экспонента
        Данные подгонки полинома квадратичной функции
        Метод интерполяции Ньютона
        Данные подгонки полинома Логарифма
        Данные подгонки полинома Кубика сплайна
    
    """
    print('выбор:[1]random')
    kln=int(input())
    if kln==1:
        M = int(input("Введите кол-во значений:"))

        matrix = []



        a, b = map(float, input("Введите интервал в виде двух чисел через пробел: ").split())



        y = []
        x = [i for i in range(0, M)]

        for i in range(M):
            k = random.uniform(a,b)

            k=round(k,4)

            y.append(k)
        x = np.array(x)
        y = np.array(y)

        print('x= ',x)
        print('y= ',y)
    if kln==2:

        from os import path

        directory = input('введите свой путь к файлу пример(matrixxx.csv)')

        if path.exists(directory):
            print('Такая папка есть')
        else:
            print('Такой папки нет')

        x = []
        y = []
        with open(directory) as csvfile:
            reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
            for row in reader:
                for i in row:
                    x.append(row[0])
                    y.append(row[1])

        del x[::2]
        del y[::2]
        print(x)
        print(y)
        M=len(x)


    def f(x):
        return np.sin(3*x) + np.cos(x)
    import csv

    def draw(x,y):
        plt.plot (x,y, label = "подгоночная кривая", color = "black")
        plt.scatter (x,y, label = "дискретные данные")
        rcParams['font.sans-serif'] = ['SimHei']
        rcParams['axes.unicode_minus'] = False
        plt.title ("Данные подгонки полинома Тригонометрия")
        plt.legend(loc="upper left")
        plt.show()
    draw(x, f(y))
    n = len(y)
    spam = list(range(1, n+1))

    rows = zip(spam,x,y, f(y))
    with open('trigonometria.csv', mode = "w") as w_file:
        tabl_writer = csv.writer(w_file, lineterminator = "\r")
        tabl_writer.writerow(["Ind", "x", "y",'kg'])
        for row in rows:
            tabl_writer.writerow(row)

    def lagran(x,y,t):
        z=0
        for j in range(len(y)):
            p1=1; p2=1
            for i in range(len(x)):
                if i==j:
                    p1=p1*1; p2=p2*1   
                else: 
                    p1=p1*(t-x[i])
                    p2=p2*(x[j]-x[i])
            z=z+y[j]*p1/p2
        return z
    xnew=np.linspace(np.min(x),np.max(x))
    ynew=[lagran(x,y,i) for i in xnew]
    plt.plot(x,y,'o',xnew,ynew)
    plt.title ("Данные подгонки полинома лагранж")
    plt.grid()
    plt.show()

    kg=lagran(x,y,[i for i in range(0, M)])


    import csv



    n = len(y)
    spam = list(range(1, n+1))

    rows = zip(spam,x,ynew, kg)
    with open('lagran.csv', mode = "w") as w_file:
        tabl_writer = csv.writer(w_file, lineterminator = "\r")
        tabl_writer.writerow(["Ind", "x", "y",'kg'])
        for row in rows:
            tabl_writer.writerow(row)

    def gaussian(x,x0,sigma):
        return np.exp(-np.power((x - x0)/sigma, 2.)/2.)



    x_values=np.linspace(np.min(x),np.max(x))
    с=[[j,k] for j,k in zip(x,y)]
    for mu, sig in с:
        t=gaussian(x,y,sig)



    n = len(y)
    spam = list(range(1, n+1))

    rows = zip(spam,x,y, t)
    with open('gaussian.csv', mode = "w") as w_file:
        tabl_writer = csv.writer(w_file, lineterminator = "\r")
        tabl_writer.writerow(["Ind", "x", "y",'t'])
        for row in rows:
            tabl_writer.writerow(row)


    def draw(x,y):
        plt.plot (x,y, label = "подгоночная кривая", color = "black")
        plt.scatter (x,y, label = "дискретные данные")
        rcParams['font.sans-serif'] = ['SimHei']
        rcParams['axes.unicode_minus'] = False
        plt.title ("Данные подгонки полинома Гаусса")
        plt.legend(loc="upper left")
        plt.show()
    draw(x_values, gaussian(x_values, mu, sig))
    def func(x, a, b, c, d):
        return a*np.exp(-c*(x*b))+d
    popt, pcov = curve_fit(func, x, y, [100,400,0.001,0])

    def draw(x,y):
        plt.plot (x,y, label = "подгоночная кривая", color = "black")
        plt.scatter (x,y, label = "дискретные данные")
        rcParams['font.sans-serif'] = ['SimHei']
        rcParams['axes.unicode_minus'] = False
        plt.title ("Данные подгонки полинома экспонента")
        plt.legend(loc="upper left")
        plt.show()
    draw(x,func(y,*popt))
    n = len(y)
    spam = list(range(1, n+1))

    rows = zip(spam,x,y, func(y,*popt))
    with open('exp.csv', mode = "w") as w_file:
        tabl_writer = csv.writer(w_file, lineterminator = "\r")
        tabl_writer.writerow(["Ind", "x", "y",'y_vals'])
        for row in rows:
            tabl_writer.writerow(row)

    def polynomial_fitting(data_x,data_y):
        size=len(data_x)
        i=0
        sum_x = 0
        sum_sqare_x =0
        sum_third_power_x = 0
        sum_four_power_x = 0
        average_x = 0
        average_y = 0
        sum_y = 0
        sum_xy = 0
        sum_sqare_xy = 0
        while i<size:
            sum_x += data_x[i]
            sum_y += data_y[i]
            sum_sqare_x += math.pow(data_x[i],2)
            sum_third_power_x +=math.pow(data_x[i],3)
            sum_four_power_x +=math.pow(data_x[i],4)
            sum_xy +=data_x[i]*data_y[i]
            sum_sqare_xy +=math.pow(data_x[i],2)*data_y[i]
            i += 1;
        average_x=sum_x/size
        average_y=sum_y/size
        return [[size, sum_x, sum_sqare_x, sum_y]
            , [sum_x, sum_sqare_x, sum_third_power_x, sum_xy]
            , [sum_sqare_x,sum_third_power_x,sum_four_power_x,sum_sqare_xy]]


    def calculate_parameter(data):

        i = 0;
        j = 0;
        line_size = len(data)


        while j < line_size-1:
            line = data[j]
            temp = line[j]
            templete=[]
            for x in line:
                x=x/temp
                templete.append(x)
            data[j]=templete

            flag = j+1
            while flag < line_size:
                templete1 = []
                temp1=data[flag][j]
                i = 0
                for x1 in data[flag]:
                    if x1!=0:
                       x1 = x1-(temp1*templete[i])
                       templete1.append(x1)
                    else:
                       templete1.append(0)
                    i += 1
                data[flag] = templete1
                flag +=1
            j += 1




        parameters=[]
        i=line_size-1

        flag_j=0
        rol_size=len(data[0])
        flag_rol=rol_size-2

        while i>=0:
            operate_line = data[i]
            if i==line_size-1:
                parameter=operate_line[rol_size-1]/operate_line[flag_rol]
                parameters.append(parameter)
            else:
                flag_j=(rol_size-flag_rol-2)
                temp2=operate_line[rol_size-1]

                result_flag=0
                while flag_j>0:
                    temp2-=operate_line[flag_rol+flag_j]*parameters[result_flag]
                    result_flag+=1
                    flag_j-=1
                parameter=temp2/operate_line[flag_rol]
                parameters.append(parameter)
            flag_rol-=1
            i-=1
        return parameters


    def calculate(data_x,parameters):
        datay=[]
        for x in data_x:
            datay.append(parameters[2]+parameters[1]*x+parameters[0]*x*x)
        return datay




    def draw(data_x,data_y_new,data_y_old):
        plt.plot (data_x, data_y_new, label = "подгоночная кривая", color = "black")
        plt.scatter (data_x, data_y_old, label = "дискретные данные")
        rcParams['font.sans-serif'] = ['SimHei']
        rcParams['axes.unicode_minus'] = False
        plt.title ("Данные подгонки полинома квадратичной функции")
        plt.legend(loc="upper left")
        plt.show()

    data=polynomial_fitting(x,y)
    parameters=calculate_parameter(data)



    newData=calculate(x,parameters)
    draw(x,newData,y)
    n = len(y)
    spam = list(range(1, n+1))

    rows = zip(spam,x,y, newData)
    with open('qudratic.csv', mode = "w") as w_file:
        tabl_writer = csv.writer(w_file, lineterminator = "\r")
        tabl_writer.writerow(["Ind", "x", "y",'newData'])
        for row in rows:
            tabl_writer.writerow(row)
    def five_order_difference_quotient(x, y):

        i = 0
        quotient = M*[0]
        while i < M-1:
            j = M-1
            while j > i:
                if i == 0:
                    quotient[j]=((y[j]-y[j-1])/(x[j]-x[j-1]))
                else:
                    quotient[j] = (quotient[j]-quotient[j-1])/(x[j]-x[j-1-i])
                j -= 1
            i += 1
        return quotient

    def function(data):
        return x[0]+parameters[1]*(data-0.4)+parameters[2]*(data-0.4)*(data-0.55)+               parameters[3]*(data-0.4)*(data-0.55)*(data-0.65)               +parameters[4]*(data-0.4)*(data-0.55)*(data-0.80)


    def calculate_data(x,parameters):
        returnData=[]
        for data in x:
            returnData.append(function(data))
        return returnData


    def draw(newData):
        plt.scatter (x, y, label = "дискретные данные", color = "red")
        plt.plot (x, newData, label = "Подгоночная кривая интерполяции Ньютона", color = "black")
        plt.title ("Метод интерполяции Ньютона")
        rcParams['font.sans-serif'] = ['SimHei']
        rcParams['axes.unicode_minus'] = False
        plt.legend(loc="upper left")
        plt.show()


    parameters=five_order_difference_quotient(x,y)



    yuanzu=calculate_data(x,parameters)
    draw(yuanzu)
    n = len(y)
    spam = list(range(1, n+1))

    rows = zip(spam,x,y, parameters)
    with open('Nyton.csv', mode = "w") as w_file:
        tabl_writer = csv.writer(w_file, lineterminator = "\r")
        tabl_writer.writerow(["Ind", "x", "y",'parameters'])
        for row in rows:
            tabl_writer.writerow(row)
    @np.vectorize
    def applog(n, x1):
        a = (1 + x1) / 2
        b = math.sqrt(x1)
        for i in range(n):
            a = (a + b) / 2
            b = math.sqrt(a * b)
        return (x1 - 1) / a

    n = len(y) 
    def draw(x,y):
        plt.plot (x,y, label = "подгоночная кривая", color = "black")
        plt.scatter (x,y, label = "дискретные данные")
        rcParams['font.sans-serif'] = ['SimHei']
        rcParams['axes.unicode_minus'] = False
        plt.title ("Данные подгонки полинома Логорифма")
        plt.legend(loc="upper left")
        plt.show()
    draw(x, applog(n, x))
    n = len(y)
    spam = list(range(1, n+1))

    rows = zip(spam,x,y, x)
    with open('Logorifm.csv', mode = "w") as w_file:
        tabl_writer = csv.writer(w_file, lineterminator = "\r")
        tabl_writer.writerow(["Ind", "x", "y",'x1'])
        for row in rows:
            tabl_writer.writerow(row)
    from typing import Tuple, List
    import bisect

    def compute_changes(x: List[float]) -> List[float]:
        return [x[i+1] - x[i] for i in range(len(x) - 1)]

    def create_tridiagonalmatrix(n: int, h: List[float]) -> Tuple[List[float], List[float], List[float]]:
        A = [h[i] / (h[i] + h[i + 1]) for i in range(n - 2)] + [0]
        B = [2] * n
        C = [0] + [h[i + 1] / (h[i] + h[i + 1]) for i in range(n - 2)]
        return A, B, C

    def create_target(n: int, h: List[float], y: List[float]):
        return [0] + [6 * ((y[i + 1] - y[i]) / h[i] - (y[i] - y[i - 1]) / h[i - 1]) / (h[i] + h[i-1]) for i in range(1, n - 1)] + [0]

    def solve_tridiagonalsystem(A: List[float], B: List[float], C: List[float], D: List[float]):
        c_p = C + [0]
        d_p = [0] * len(B)
        X = [0] * len(B)

        c_p[0] = C[0] / B[0]
        d_p[0] = D[0] / B[0]
        for i in range(1, len(B)):
            c_p[i] = c_p[i] / (B[i] - c_p[i - 1] * A[i - 1])
            d_p[i] = (D[i] - d_p[i - 1] * A[i - 1]) / (B[i] - c_p[i - 1] * A[i - 1])

        X[-1] = d_p[-1]
        for i in range(len(B) - 2, -1, -1):
            X[i] = d_p[i] - c_p[i] * X[i + 1]

        return X

    def compute_spline(x: List[float], y: List[float]):
        n = len(x)
        if n < 3:
            raise ValueError('Too short an array')
        if n != len(y):
            raise ValueError('Array lengths are different')

        h = compute_changes(x)


        A, B, C = create_tridiagonalmatrix(n, h)
        D = create_target(n, h, y)

        M = solve_tridiagonalsystem(A, B, C, D)

        coefficients = [[(M[i+1]-M[i])*h[i]*h[i]/6, M[i]*h[i]*h[i]/2, (y[i+1] - y[i] - (M[i+1]+2*M[i])*h[i]*h[i]/6), y[i]] for i in range(n-1)]

        def spline(val):
            idx = min(bisect.bisect(x, val)-1, n-2)
            z = (val - x[idx]) / h[idx]
            C = coefficients[idx]
            return (((C[0] * z) + C[1]) * z + C[2]) * z + C[3]

        return spline


    x = [i for i in range(0, M)]
    spline = compute_spline(x, y)
    colors = 'r'
    for i, x in enumerate(x):
        assert abs(y[i] - spline(x)) < 1e-8, f'Error at {x}, {y[i]}'

    x_vals = [v / 10 for v in range(M)]
    y_vals = [spline(y) for y in x_vals]
    plt.scatter(x_vals,y_vals,c=colors)
    plt.title ("Данные подгонки полинома Кубика сплайна")
    plt.plot(x_vals,y_vals,'g')
    n = len(y)
    spam = list(range(1, n+1))

    rows = zip(spam,x_vals,y, y_vals)
    with open('Cubic.csv', mode = "w") as w_file:
        tabl_writer = csv.writer(w_file, lineterminator = "\r")
        tabl_writer.writerow(["Ind", "x", "y",'y_vals'])
        for row in rows:
            tabl_writer.writerow(row)
            
print(interpol.__doc__)