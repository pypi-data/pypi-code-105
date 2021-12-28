import numpy as np 


def vv(ex):
    if ex.shape == (2, 2):
        #print(ex, '\n', ex[0, 0] * ex[1, 1] - ex[1, 0] * ex[0, 1])
        return ex[0, 0] * ex[1, 1] - ex[1, 0] * ex[0, 1];
    else:
        a = 0
        for j in range(ex.shape[0]):
            if j == 0:
                a += np.power(-1, j+2) * ex[0, j] * vv(ex[1:, 1:])
            elif j == (ex.shape[0]-1): 
                a += np.power(-1, j+2) * ex[0, j] * vv(ex[1:,:-1])
            else:
                a += np.power(-1, j+2) * ex[0, j] * vv(np.hstack((ex[1:, :j], ex[1:, j+1:])))
    return a
print(a)
print(vv(a)) 

def vv(ex):
    if ex.shape == (1, 1):
        #print(ex, '\n', ex[0, 0] * ex[1, 1] - ex[1, 0] * ex[0, 1])
        #return ex[0, 0] * ex[1, 1] - ex[1, 0] * ex[0, 1];
        return ex[0, 0]
    else:
        a = 0
        for j in range(ex.shape[0]):
            if j == 0:
                a += np.power(-1, j+2) * ex[0, j] * vv(ex[1:, 1:])
            elif j == (ex.shape[0]-1): 
                a += np.power(-1, j+2) * ex[0, j] * vv(ex[1:,:-1])
            else:
                a += np.power(-1, j+2) * ex[0, j] * vv(np.hstack((ex[1:, :j], ex[1:, j+1:])))
    print(a)
    return a
    
#np.random.seed(42)    
#a = np.random.randint(10, size = (3, 3))
#print(a)
#print(vv(a))


# С клавиатуры вводится матрица nm Вывести транспонированную +могут быть комплексные
# 
# Матричное преобразование квадратных матриц 5на5 - сложить умножить вычесть Пользователь вводит выражение, потом размерность, потом цикл
# 
# Матрица квадратная, надо считать определитель рекурсивным алгоритмом. Мы берём определить и раскладываем по первой строке, когда 1на1 останавливается


def mat():
    row1 = int(input(f'Введите кол-во строк первой матрицы '));#строки матрицы 1
    col1 = int(input(f'Введите кол-во столбцов первой матрицы '));#столбцы матрицы 1
    row2 = int(input(f'Введите кол-во строк второй матрицы '));#строки матрицы 2 
    col2 = int(input(f'Введите кол-во столбцов второй матрицы '));#столбцы матрицы 2
    act = input(f'Введите одно из следующих действий: +, -, *, .T \nВы ввели: ');#действие которое будет производится с матрицей сюда можно ввести: *, -, +
    x1 = [];
    x2 = [];
    for i in range(row1):
        y1 = [];
        for j in range(col1):
            y1.append(complex(input(f'Введите данные для строки: {i}, и для стобца: {j}. ')));
        x1.append(y1);
    for i in range(row2):
        y2 = [];
        for j in range(col2):
            y2.append(complex(input(f'Введите данные для строки: {i}, и для стобца: {j}. ')));
        x2.append(y2);
    x1 = np.array(x1);
    x2 = np.array(x2);
    if act == '*':
        return x1.dot(x2);#
    elif act == '-':
        return x1-x2;
    elif act == '+':
        return np.array(sum(x1, x2));
    elif act == '.T' and row2 == col2 and col2 == 0:
        return np.transpose(x1);#.transpose(.T) - транспонирование матриц
    else:
        print('Вы ввели не корректно введите все значения заново.');


#print(mat())


# print(np.matrix(x).T);# .T - транспонирование матриц



# 
