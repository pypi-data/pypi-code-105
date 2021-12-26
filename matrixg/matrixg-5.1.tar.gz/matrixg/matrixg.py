import random
import numpy as np
import csv 
import fractions
from scipy.linalg import solve
import time

def matrix_1(): 
    """FUNCTIONS:
    matrixg.matrix_1() - основная работа программы
    выполнять решать СЛАУ методом
    Gaussa and Jacoby
    authors:
        Shpeka,Chernov,Kaxorov,Martishenya
    """
    print(matrix_1.__doc__)
    matrix=[] 
    def minor(array):
        """функция minor нужна чтобы найти определитель если матрица 2x2"""
        return array[0][0] * array[1][1] - array[1][0] * array[0][1] 
    def division(array):
        """division нужен чтобы решать матрицу 3x3 и тд"""
        if len(array[0]) > 2:
            result = 0
            for i in range(len(array[0])):
                new_arr = []
                for j in range(len(array[0])):
                    if j != i:
                        new_arr.append([array[j][k] for k in range(1, len(array[0]))])
                result += division(new_arr) * array[i][0] * (-1 + 2 * ((i + 1) % 2))
            return result
        else:
            return minor(array)
    def makeTriangleNaive(matrix):
        """ функция меняет матрицу через побочные эффекты
            nrow равен номеру строки
            row содержит саму строку матрицы"""
        
        for nrow, row in enumerate(matrix):
           
            divider = row[nrow]
            if divider==0:
                row =divider/ row
            else:
                row =row/ divider
            # теперь надо вычесть приведённую строку из всех нижележащих строчек
            for lower_row in matrix[nrow+1:]:
                factor = lower_row[nrow] # элемент строки в колонке nrow
                lower_row -= factor*row # вычитаем, чтобы получить ноль в колонке nrow
        # все строки матрицы изменились, в принципе, можно и не возвращать
        return matrix
    makeTriangleNaive(matrix.copy())
    def makeIdentity(matrix):
        """перебор строк в обратном порядке"""
        for nrow in range(len(matrix)-1,0,-1):
            row = matrix[nrow]
            for upper_row in matrix[:nrow]:
                factor = upper_row[nrow]
                # вычитать строки не нужно, так как в row только два элемента отличны от 0:
                # в последней колонке и на диагонали
                if matrix[0][0]==0:
                # вычитание в последней колонке
                    upper_row[1] -= factor*row[-1]
                else:
                    upper_row[-1] -= factor*row[-1]
                # вместо вычитания 1*factor просто обнулим коэффициент в соотвествующей колонке. 
                upper_row[nrow] = 0
        return matrix
    def makeTrianglePivot(matrix):
        for nrow in range(len(matrix)):
            # nrow равен номеру строки
            # np.argmax возвращает номер строки с максимальным элементом в уменьшенной матрице
            # которая начинается со строки nrow. Поэтому нужно прибавить nrow к результату
            pivot = nrow + np.argmax(abs(matrix[nrow:, nrow]))
            if pivot != nrow:
                # swap
                # matrix[nrow], matrix[pivot] = matrix[pivot], matrix[nrow] - не работает.
                # нужно переставлять строки именно так, как написано ниже
                # matrix[[nrow, pivot]] = matrix[[pivot, nrow]]
                matrix[nrow], matrix[pivot] = matrix[pivot], np.copy(matrix[nrow])
            row = matrix[nrow]
            divider = row[nrow] # диагональный элемент
            if abs(divider) < 1e-10:
                # почти нуль на диагонали. Продолжать не имеет смысла, результат счёта неустойчив
                raise ValueError("Матрица несовместна")
            # делим на диагональный элемент.
            if divider==0:
                row =divider/ row
            else:
                row =row/ divider
            # теперь надо вычесть приведённую строку из всех нижележащих строчек
            for lower_row in matrix[nrow+1:]:
                factor = lower_row[nrow] # элемент строки в колонке nrow
                lower_row =- factor*row # вычитаем, чтобы получить ноль в колонке nrow
        return matrix


    def gaussSolveNaive(A, b=None):
        """Решает систему линейных алгебраических уравнений Ax=b
        Если b is None, то свободные коэффициенты в последней колонке"""

        shape = A.shape
        assert len(shape) == 2, ("Матрица не двумерная", shape) # двумерная матрица
        A = A.copy()
        if b is not None:
            assert shape[0] == shape[1], ("Матрица не квадратная", shape)
            assert b.shape == (shape[0],), ("Размерность свободных членов не соответствует матрица", shape, b.shape)
            # добавляем свободные члены дополнительным столбцом
            A = np.c_[A, b]
        else:
            # Проверяем, что квадратная плюс столбец
            assert shape[0]+1 == shape[1], ("Неверный формат матрицы", shape)
        makeTriangleNaive(A)
        makeIdentity(A)

        return A[:,-1]
    def Jacoby(A,b,x,n):
        """Решает матрицу по Jacoby"""

        D=np.diag(A)
        R=A-np.diagflat(D)
        for i in range(n):
            x=(b-np.dot(R,x))/D
        return(x)
    def frac(x):
        """функция frac преобразовывет ввод дробных чисел
        например: 3/5 он преобразует в 0.6"""
        np.set_printoptions(formatter = {
           'all': lambda x: str(fractions.Fraction(x))
        })
        return x
    def visual():
        """Рисует красивую систему равнений"""
        print("System:" )
        for i in range(A.shape[0]):
            row = ["{}*x{}" .format(A[i, j], j + 1) for j in range(A.shape[1])]
            print(" + ".join(row), "=", b[i])
        return    


    print("Будут ли у вас дроби:[1]Да/[2]Нет")
    g=int(input())
    if g==1:
        print('как вы хотите заполнять матрицу([1]:с клавиатуры/[2]:random ')
        p = int(input())
        M = int(input("Введите количество строк:"))
        N = int(input("Введите количество столбцом:"))
        b=[]
        if p==1:

            for i in range(M):          
                a =[]

                for j in range(N):
                    a.append(eval(input("Vvedite chisla primer(3/5)= ")))

                matrix.append(a)



        if p==2:
                a2, b2 = map(float, input("Введите интервал в виде двух чисел через пробел: ").split()) 
                for i in range(M):          
                    a=[]

                    for j in range(N):
                            r = random.randint(a2,b2)
                            a.append(r)

                    matrix.append(a)
        for i in range(M):        
            b.append(eval(input('vector')))

        matrix2 = np.array(matrix)
        tr = matrix2.transpose()
        tr1=tr/division(matrix)
        print('Обратная матрица')
        print(tr1)
        print("Cord= ",cord)
        print("Решение по функции Гаусса Fractions")

        l=frac(matrix)



        #print(mat)
        #l1=np.array(l)
        print(l, end=' ') 
        b1=np.array(b)




        print('с доп столбцом')
        c=np.column_stack([frac(matrix), b])
        print(c)



        print('solution',gaussSolveNaive(c))
    if g==2:
        print("Будут ли у вас комплексные числа:[1]да/[2]нет ")
        j=int(input())
        if j==1:
            print('как вы хотите заполнять матрицу([1]:с клавиатуры/[2]:random ')
            p = int(input())
            M = int(input("Введите количество строк:"))
            N = int(input("Введите количество столбцом:"))
            b=[]

            matrix=[]

            if p==1:

                for i in range(M):          
                        a =[]

                        for j in range(N):
                            a.append(complex(input()))

                        matrix.append(a)




            if p==2:
                a2, b2 = map(float,input("Введите интервал в виде двух чисел через пробел: ").split()) 
                for i in range(M):          
                    a=[]

                    for j in range(N):
                            r = random.randint(a2,b2)
                            a.append(r)

                    matrix.append(a)
            for i in range(M):        
                b.append(complex(input('vector')))
            c=np.column_stack([matrix, b])
            matrix2 = np.array(matrix)
            print(c)
            tr = matrix2.transpose()
            tr1=tr/division(matrix)
            print('Обратная матрица')
            print(tr1)
            norm1 = np.linalg.norm(matrix2)
            norm2 = np.linalg.norm(tr1)
            cord = norm1*norm2
            A=matrix2
            x=M
            n=25




            print("Решение по функции Якоби", visual(), solve(A,b))
            print("Cord= ",cord)
            if cord<100:
                print('Дальнейшие вычисления не требуются')
                if cord>100:

                    print(tr1)
                    print("Cord= ",cord)
                    print("Решение по функции Гаусса",gaussSolveNaive(matrix2))    
            if cord>100:
                for i in c:
                    print(i)
                print(tr1)
                print("Cord= ",cord)
                print("Решение по функции Гаусса Fractions")
                l=frac(matrix2)
                print(gaussSolveNaive(l))
        if j==2:

            print('как вы хотите заполнять матрицу([1]:с клавиатуры/[2]:random ')
            p = int(input())

            b=[]
            if p==1:
                M = int(input("Введите количество строк:"))
                N = int(input("Введите количество столбцом:"))
                for i in range(M):          
                    a =[]

                    for j in range(N):
                        a.append(float(input("Vvedite chisla primer(3/5)= ")))

                    matrix.append(a)



            if p==2:
                    M = int(input("Введите количество строк:"))
                    N = int(input("Введите количество столбцом:"))
                    a2, b2 = map(float, input("Введите интервал в виде двух чисел через пробел: ").split()) 
                    for i in range(M):          
                        a=[]

                        for j in range(N):
                                r = random.randint(a2,b2)
                                a.append(r)

                        matrix.append(a)

            for i in range(M):        
                b.append(float(input('vector')))
            c=np.column_stack([matrix, b]) 
            for i in c:
                print(i)

            matrix2 = np.array(matrix)
            tr = matrix2.transpose()
            tr1=tr/division(matrix)
            print('Обратная матрица')
            print(tr1)
            norm1 = np.linalg.norm(matrix2)
            norm2 = np.linalg.norm(tr1)
            cord = norm1*norm2
            print("Cord= ",cord)

            A=matrix2
            x=M
            n=25

            t1=time.perf_counter()
            print("Решение по функции Якоби",visual(), solve(A,b))

            t2=time.perf_counter()
            print(t2-t1)
            print("Cord= ",cord)
            if cord<100:
                print('Дальнейшие вычисления не требуются')
            else:

                    print(tr1)
                    print("Cord= ",cord)
                    t1=time.perf_counter()

                    print("Решение по функции Гаусса",gaussSolveNaive(c)) 
                    t2=time.perf_counter()
                    print(t2-t1)
            if cord>100:
                for i in c:
                    print(i)
                print(tr1)
                print("Cord= ",cord)
                t1=time.perf_counter()
                #timer3 = time.time()
                print("Решение по функции Гаусса Fractions")
                l=frac(matrix2)
                c=np.column_stack([l, b])
                print(gaussSolveNaive(c))
                t2=time.perf_counter()
                print(t2-t1)
                

print(matrix_1.__doc__)
__all__=['matrix_1']
