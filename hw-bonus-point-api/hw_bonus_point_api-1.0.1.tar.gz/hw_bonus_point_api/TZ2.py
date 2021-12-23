#!/usr/bin/env python
# coding: utf-8

# №1. Транспонирование матрицы

# In[ ]:


# Вариант после исправления:
import numpy as np
row = int(input("Введите количество строк: "))  
column = int(input("Введите количество столбцов: "))  
 
matrix = []  
print("Заполните матрицу по одному элементу: ")  
 
for i in range(row):         
    a =[]  
    for j in range(column):      
        a.append(int(input()))  
    matrix.append(a)  
 
   
for i in range(row):  
    for j in range(column):  
        print(matrix[i][j], end = " ")  
    print()  
A1 = np.matrix(matrix)
Tr_A = A1.getT()
print('Исходная матрица: ', matrix)
print('Транспонированная матрица: ', Tr_A)


# Исходный вариант задания №1(до исправления):

# import numpy as np
# n, m = map(int, input("Введите кол-во строк и столбцов через пробел: ").split())
# A = list(map(int,input('Заполните матрицу через пробел: ').split()))
# A = [A[j * m : (j + 1) * m] for j in range(n)]
# A0 = A
# A1 = np.matrix(A)
# Tr_A = A1.getT()
# print('Исходная матрица: ', A0)
# print('Транспонированная матрица: ', Tr_A)

# №2. Матричное преобразование квадратных матриц 5 х 5 (Исправленый вариант по способу заполнения матрицы + вычисление норм матрицы и детерминанта)

# In[ ]:


#Вариант после исправления
import numpy as np
from numpy.linalg import norm
row = int(input("Введите количество строк первой матрицы: "))  
column = int(input("Введите количество столбцов первой матрицы: "))  
 
matrix = []  
print("Заполните матрицу по одному элементу: ")  
 
for i in range(row):         
    a =[]  
    for j in range(column):      
        a.append(int(input()))  
    matrix.append(a)  
 
 
for i in range(row):  
    for j in range(column):  
        print(matrix[i][j], end = " ")  
    print()  
A1 = np.matrix(matrix)

row2 = int(input("Введите количество строк второй матрицы: "))  
column2 = int(input("Введите количество столбцов второй матрицы: "))  
 
matrix2 = []  
print("Заполните матрицу по одному элементу: ")  
 
for i in range(row2):         
    a2 =[]  
    for j in range(column2):      
        a2.append(int(input()))  
    matrix2.append(a2)  
for i in range(row2):  
    for j in range(column2):  
        print(matrix2[i][j], end = " ")  
    print()  
B1 = np.matrix(matrix2)
znak = input('''Выберите '*'(умножение),'+'(сложение),'-'(вычитание), OPR(вычисление детерминанта),N2(сумма модулей элементов столбца): ''')
if znak == '*':
    if column != row2:
        print('Количество столбцов первой матрицы не равно количеству строк второй матрицы! Операция невозможа.')
    else:
        print('Результат умножения матриц:')
        print(A1*B1)
elif znak == '+':
    print('Результат сложения матриц:')
    print(A1+B1)
elif znak == '-':
    print('Результат вычитания матриц:')
    print(A1-B1) 
elif znak == 'OPR':
    print('Детерминант первой матрицы: ', np.linalg.det(A1))
    print('Детерминант второй матрицы: ', np.linalg.det(B1))
elif znak == 'N2':
    #Для первой матрицы
    if column and column2 == 2:
        fr2 = int(sum(A1[:,0]))
        se2 = int(sum(A1[:,1]))
        fr2_B = int(sum(B1[:,0]))
        se2_B = int(sum(B1[:,1]))
        print(max(fr2,se2))
        print(max(fr2_B,se2_B))
    elif column and column2 == 3:
        fr3 = int(sum(A1[:,0]))
        se3 = int(sum(A1[:,1]))
        th3 = int(sum(A1[:,2]))
        fr3_B = int(sum(B1[:,0]))
        se3_B = int(sum(B1[:,1]))
        th3_B = int(sum(B1[:,2]))
        print(max(fr3,se3,th3))
        print(max(fr3_B,se3_B,th3_B))
    elif column and column2 == 4:
        fr4 = int(sum(A1[:,0]))
        se4 = int(sum(A1[:,1]))
        th4 = int(sum(A1[:,2]))
        fo4 = int(sum(A1[:,3]))
        fr4_B = int(sum(B1[:,0]))
        se4_B = int(sum(B1[:,1]))
        th4_B = int(sum(B1[:,2]))
        fo4_B = int(sum(B1[:,3]))
        print(max(fr4,se4,th4,fo4))
        print(max(fr4_B,se4_B,th4_B,fo4_B))
    elif column and column2 == 5:
        fr5 = int(sum(A1[:,0]))
        se5 = int(sum(A1[:,1]))
        th5 = int(sum(A1[:,2]))
        fo5 = int(sum(A1[:,3]))
        fi5 = int(sum(A1[:,4]))
        fr5_B = int(sum(B1[:,0]))
        se5_B = int(sum(B1[:,1]))
        th5_B = int(sum(B1[:,2]))
        fo5_B = int(sum(B1[:,3]))
        fi5_B = int(sum(B1[:,4]))
        print(max(fr5,se5,th5,fo5,fi5))
        print(max(fr5_B,se5_B,th5_B,fo5_B,fi5_B))
  


# # Исходный вариант задания №2(до исправления):
# import numpy as np
# n, m = map(int, input("Введите кол-во строк и столбцов для первой (А) матрицы  через пробел: ").split())
# znak = input('''Выберите '*'(умножение),'+'(сложение),'-'(вычитание): ''')
# A = list(map(int,input('Заполните матрицу через пробел: ').split()))
# A = [A[j * m : (j + 1) * m] for j in range(n)]
# A1 = np.matrix(A)
# n1,m1 = map(int, input("Введите кол-во строк и столбцов для второй (В) матрицы  через пробел: ").split())
# B = list(map(int,input('Заполните матрицу B через пробел: ').split()))
# B = [B[j * m1 : (j + 1) * m1] for j in range(n1)]
# B1 = np.matrix(B)
# if znak == '*':
#     if m != n1:
#         print('Количество столбцов первой матрицы не равно количеству строк второй матрицы! Операция невозможа.')
#     else:
#         print('Результат умножения матриц:')
#         print(A1*B1)
# elif znak == '+':
#     print('Результат сложения матриц:')
#     print(A1+B1)
# elif znak == '-':
#     print('Результат вычитания матриц:')
#     print(A1-B1)
# 
