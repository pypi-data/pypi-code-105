import numpy as np
import numexpr as ne
from math import *
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import mpmath as mp
def oderk3():
    def euler(x0, y0, xn, n):

        h= (xn- x0)/ n #здесь считаем размерность шага

        print('____________________')
        print('x0\ty0\tslope\tyn')
        print('----------------------')

        for _ in range(n):
            slope= f(x0, y0)
            yn= y0+ h* slope
            print('%.4f\t%.4f\t%0.4f\t%.4f'% (x0, y0, slope, yn) )
            print('------------------------------')
            y0= yn
            x0= x0+h

        print('\nAt X= %.4f, Y= %.4f' %(xn, yn))
        #plt.plot(x0, y0)
        #plt.ezplot(x0)
    #euler(x0,y0,xn,step)
    def vis(f, xn, x0, n):
        plt.style.use('seaborn-poster')

        #f = eval('lambda x, y: '+input('Введите уравнение с переменными x и y: ')) 
        h= (xn- x0)/ n 
        x = np.arange(0, 1 + h, h) #числовая сетка/матрица ккоэффициентов
        s0 = -1

        y = np.zeros(len(x))
        y[0] = s0

        for i in range(0, len(x) - 1):
            y[i + 1] = y[i] + h*f(x[i], y[i])

        plt.figure(figsize = (12, 8))
        plt.plot(x, y, 'bo--')


        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.grid()
        plt.legend(loc='lower right')
        plt.show()
    def tRK(dydx, f , x0, y0, xn, step):

        #print('Если вы вводите тригонометрические, то вводите так: np.sin() и тд')
        #dydx= eval('lambda x, y: '+input('введите уравнение с переменными y и x: '))
        #f= eval('lambda x: '+input(' введите уравнение с переменными  x: '))


        def RK3(x, y, h):
        # скудная аппроксимация
            k_1 = dydx(x, y)
            k_2 = dydx(x+h/2, y+(h/2)*k_1)
            k_3 = dydx(x+h/2, y+h*(-k_1 + 2*k_2))

        # расчитываем новый y
            y = y + h * (1/6) * (k_1 + 4 * k_2 + k_3)
            return y


        def RK4(x, y, h):

            k_1 = dydx(x, y)
            k_2 = dydx(x+h/2, y+(h/2)*k_1)
            k_3 = dydx(x+h/2, y+(h/2)*k_2)
            k_4 = dydx(x+h, y+h*k_3)


            y = y + h * (1/6)*(k_1 + 2*k_2 + 2*k_3 + k_4)
            return y


    # инициализация
        h=step
        n = step
        x = x0                     
        y = y0
        y_rk3 = xn

        print("x \t\t yRK3 \t\t yRK4 \t\t f(x)")
        print(f"{round(x, 3):.1f} \t\t {round(y_rk3, 3):4f} \t\t {round(y, 3):4f} \t\t {round(f(x, y), 3):.4f}")

        x_plot = []
        y_RK3 = []
        y_RK4 = []
        y_analytical = []



        for i in range(0, n):

            x_plot.append(x)
            y_RK4.append(y)
            y_RK3.append(y_rk3)
            y_analytical.append(f(x,y))


            y = RK4(x, y, h)
            y_rk3 = RK3(x, y_rk3, h)

            x += h
            print(f"{round(x, 3):.1f} \t\t {round(y_rk3, 3):4f} \t\t {round(y, 3):4f} \t\t {round(f(x, y), 3):.4f}")


        x_plot.append(x)
        y_RK3.append(y_rk3)
        y_RK4.append(y)
        y_analytical.append(f(x,y))


    # визуализация
        fig, (ax, ax2) = plt.subplots(2, 1, figsize= (25, 15))
        ax.plot(x_plot, y_analytical, 'o-r', label='Analytical solution')
        ax.plot(x_plot, y_RK4, '.-b', label='Fourth-order Runge-Kutta estimate')
        ax.plot(x_plot, y_RK3, '.-g', label='Third-order Runge-Kutta estimate')
        ax.set_ylabel("y", fontsize=18)
        ax.grid()
        ax.legend()

        ax2.plot(x_plot, abs(np.array(y_analytical) -
                            np.array(y_RK4)), '.-b', label='Fourth-order Runge-Kutta')
        ax2.plot(x_plot, abs(np.array(y_analytical) -
                            np.array(y_RK3)), '.-g', label='Third-order Runge-Kutta')
        ax2.set_ylabel("Abs Error", fontsize=25)
        ax2.legend()
        ax2.set_xlabel("x", fontsize=25)
        ax2.grid()

    def predict(x, y, h): 
        #как видно из названия, функция служит в качестве "предсказания" следующдего числа
        #да и размер шага тоже
        y1p= y+ h* f(x, y);
        return y1p;

    def correct(x, y, x1, y1, h):
        #функция корректировки предсказанного значения
        e= 0.00001;
        y1c= y1;

        while (abs(y1c- y1)> e + 1):
            y1= y1c;
            y1c= y+ 0.5* h* (f(x, y)+ f(x1, y1));
        #корректировка каждого значения итерации
        return y1c;
    def correct2(x, y, x1, y1, h, y1c):
        e= 0.00000001;
        y1c= y1;
        while (abs(y1c- y1)> e + 0.1):
            y1= y1c;
            y1c= y+ 0.5* h* (f(x, y)+ f(x1, y1));
        #корректировка каждого значения итерации
        return y1c;

    def printFinalValues(x, xn, y, h):
        n= step
        h= (xn- x0)/ n
        xn= xn
        x= x0
        y= y0
        while (x < xn):
            x1= x + h;
            y1p= predict(x, y, h);
            y1c= correct(x, y, x1, y1p, h);
            y1c= correct2(x, y, x1, y1p, h, y1c);
            x= x1;
            y= y1c;
        print('____________________')
        print("Финальное значение y по x =",
                         x0, "это :", y);
        x_plot = []
        y_correct = []
        y_predict = []
        for i in range(1, n+ 1):
            x_plot.append(x)
            y_correct.append(y1c) 
            y_predict.append(y1p)  
            y= y1c  
            x += h
        x_plot.append(x)
        y_correct.append(y1c)
        y_predict.append(y1p)
        #print(x_plot)
        #print(type(x_plot))
        #print(y)
        #print(type(y))
        #print(y1c)
        #print(type(y1c))
        #print(y_correct)
        #print(type(y_correct))
        #print(y_predict)
        #print(type(y_predict))
    # визуализация
        fig, ax= plt.subplots(1, 1, figsize= (14, 10))
        ax.plot(x_plot, 'o-r', label='True')
        ax.plot(x_plot, y_correct, '.-b', label='Correct')
        ax.plot(x_plot, y_predict, '.-g', label='Predicted')
        ax.set_ylabel("y", fontsize=18)
        ax.grid()
        ax.legend()

        #plt.figure(figsize= (14,4))
        #plt.plot(x1, y1c)
    #printFinalValues(x, xn, y, h)
    def pikar():
        h= 1./step
        xs= np.linspace(0, 1, step+ 1) #узлы
        plt.figure(figsize= (14, 4))
        for i in range(1, step):
            phi= (np.zeros(xs.shape))
            phi[i]= 1
            if i== 4:
                plt.plot(xs,phi, 'r-o')
            else:
                plt.plot(xs,phi, 'b-o')
                plt.plot(xs,phi, 'black')
        plt.title(r'График базисной функции', fontsize= 22)
        plt.text(4./step, 1.4, r'$\phi_4$', fontdict ={'color':'red','size':24})
        plt.xlabel(r'$x$')
        plt.axis([0,1,0,2])
        plt.ylabel(r'$\phi_i(x)$')
        plt.grid()
        plt.show()
        A= (np.diag(2*np.ones(step-1)) + np.diag(-np.ones(step- 2),1) + np.diag(-np.ones(step- 2),-1))/ h
        print('____________________')
        print("Матрица жесткости: \n", A)
    def vis2(f, xn, x0, n):

        #f = eval('lambda x, y: '+input('Введите уравнение с переменными x и y: ')) 
        h= (xn- x0)/ n 
        x = np.arange(0, 1 + h, h) #числовая сетка/матрица ккоэффициентов
        s0 = -1

        y = np.zeros(len(x))
        y[0] = s0

        for i in range(0, len(x) - 1):
            y[i + 1] = y[i] + h*f(x[i], y[i])

        plt.figure(figsize = (12, 8))
        plt.plot(x, y, 'ro--')


        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.grid()
        plt.legend(loc='lower right')
        plt.show()



    print('Мы можем и не можем: ')
    print('[1] - функция двух переменных ') 
    #print('[2] - уравнение (Не реализовано)')
    #print('[3] - система уравнений (Не реализовано)') 
    print('--------------------')
    choose= int(input('Выберете действие: '))
    print('____________________')
    print('[1] - Эйлера-Коши; [2] -  Рунге-Кутты; [3] - Конечный элемент; [4] - Пикара')
    choose2= int(input('Выберете способ решения: '))
    print('--------------------')
    if choose== 1:
        if choose2== 1:
            print('Введите уравнение ниже..')
            f= eval('lambda x, y: '+input(' '))
            print('----------------------')
            x0= float(input('Введите начальные условия по x0= '))
            y0= float(input('Введите начальные условия по y0= '))
            print('----------------------')
            print('Введите интервал')
            xn= float(input('Кол-во точек счета = '))
            step= int(input('Кол-во шагов = '))
            euler(x0,y0,xn,step)
            vis(f, xn, x0, step)
            #plt.plot(x0,y0)
        if choose2== 2:

            dydx= eval('lambda x, y: '+input('Введите уравнение с переменными y и x: '))
            print('----------------------')
            x0= float(input('Введите начальные условия по x0= '))
            y0= float(input('Введите начальные условия по y0= '))
            print('----------------------')
            print('Введите интервал')
            xn= float(input('Кол-во точек счета = '))
            step= int(input('Кол-во шагов = '))
            #f= eval('lambda x,y: '+input('Введите уравнение с переменными  x: '))
            f= dydx
            tRK(dydx, f, x0, y0, xn, step)
        if choose2== 3:
            print('Введите уравнение ниже..')
            f= eval('lambda x, y: '+input(' '))
            print('----------------------')
            x0= float(input('Введите начальные условия по x0= '))
            y0= float(input('Введите начальные условия по y0= '))
            print('----------------------')
            print('Введите интервал')
            xn= float(input('Кол-во точек счета = '))
            step= int(input('Кол-во шагов = '))
            printFinalValues(x0, xn, y0, step)
            #plt.plot(x0,y0)
        if choose2== 4:
            print('Введите уравнение ниже..')
            f= eval('lambda x, y: '+input('Введите уравнение с переменными x и y: '))
            z= eval('lambda x: '+input('Введите уравнение с переменными x: '))
            print('----------------------')
            x0= float(input('Введите начальные условия по x0= '))
            y0= float(input('Введите начальные условия по y0= '))
            print('----------------------')
            print('Введите интервал')
            xn= float(input('Кол-во точек счета = '))
            step= int(input('Кол-во шагов = '))
            print('----------------------')
            print('Решение: ')
            print('y(', x0,',', y0, ') = ',f(x0, y0)+ z(x0))
            pikar()
            vis2(f, xn, x0, step)
            #plt.plot(x0,y0)
    if choose== 2:
        print('Введите функцию ниже..')
        starting_function= input(' ')
        print('----------------------')
        x= int(input('Введите начальные условия по x0= '))
        y= int(input('Введите начальные условия по y0= '))
        print('Введите начальный интервал от _ до')
        started= []
        for w in range(2):
            pusher= int(input('--> '))
            started.append(pusher)
        print('----------------------')
    if choose== 3:
        print('Введите количество уравнений в системе..')
        co= int(input('= '))
        stack_ec= []
        for _ in range(co):
            starting_function= input(' ')
            stack_ec.append(starting_function)
        print(stack_ec)
        print('----------------------')
        x= int(input('Введите начальные условия по x0= '))
        y= int(input('Введите начальные условия по y0= '))
        print('Введите начальный интервал от _ до')
        started= []
        for w in range(2):
            pusher= int(input('--> '))
            started.append(pusher)
        print('----------------------')

