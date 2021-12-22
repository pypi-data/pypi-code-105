from .Fraction import Fraction
from .ComplexFraction import ComplexFraction


class Matrix:
    def __init__(self, m=1, n=1):
        __slots__ = 'self'
        assert n > 0, 'Неверные данные'
        assert m > 0, 'Неверные данные'
        assert isinstance(n, int), 'Неверные данные'
        assert isinstance(m, int), 'Неверные данные'

        if n >= 0 and m >= 0:
            self.n = n
            self.m = m
            self.matrix = [[0] * n] * m
            self.is_complex = False

    def __getitem__(self, key):
        return self.matrix[key]

    def __setitem__(self, key, value):
        self.matrix[key] = value

    def __len__(self):
        return len(self.matrix)

    @staticmethod
    def get_from_list(list_):
        if not Matrix.__check_shape(list_):
            raise Exception("Ошибка: строки разной длины")
        matrix = Matrix()
        matrix.matrix = list_
        matrix.n = len(list_)
        matrix.m = len(list_[0])
        return matrix

    @staticmethod
    def __check_shape(list_):
        c = len(list_[0])
        for i in range(1, len(list_)):
            if c != len(list_[i]):
                return False
        return True

    @staticmethod
    def get_minor(matrix, i, j):
        return [row[:j] + row[j + 1:] for row in (matrix[:i] + matrix[i + 1:])]

    def transpose(self):
        matrix_T = [[0 for j in range(len(self))] for i in range(len(self[0]))]

        for i in range(len(self[0])):
            for j in range(len(self)):
                matrix_T[i][j] = self[j][i]

        return Matrix.get_from_list(matrix_T)

    def shape(self):
        return len(self), len(self[0])

    def __get_op(self, other, op):
        n, m = self.shape()
        if isinstance(other, float) or isinstance(other, int) or isinstance(other, complex):
            result = [[op(other, self[i][j]) for j in range(m)] for i in range(n)]
        else:
            if self.shape() == other.shape():
                result = [[op(other[i][j], self[i][j]) for j in range(m)] for i in range(n)]
            else:
                raise BaseException('Неправильная размерность матрицы')
        return Matrix.get_from_list(result)

    def __add__(self, other):
        return self.__get_op(other, lambda x, y: x + y)

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        if isinstance(self, Matrix) and isinstance(other, Matrix):
            return Matrix.dot(self, other)
        return self.__get_op(other, lambda x, y: x * y)

    def __rmul__(self, other):
        if isinstance(self, Matrix) and isinstance(other, Matrix):
            return Matrix.dot(self, other)
        return self * other

    def __sub__(self, other):
        return self + (-1) * other

    def __rsub__(self, other):
        return self.__get_op(other, lambda x, y: y - x)

    def __floordiv__(self, other):
        return self.__get_op(other, lambda x, y: x // y)

    def __rfloordiv__(self, other):
        return self // other

    def __truediv__(self, other):
        return self.__get_op(other, lambda x, y: x / y)

    def __rtruediv__(self, other):
        return self / other

    def __best_line(self):
        """Нахождение лучшей строки для вычисления определителя"""
        h_dict = {}
        for k, v in enumerate(self):
            maxim = v.count(0)
            sp = [i for i in h_dict.values()]
            if len(h_dict) != 0:
                if sp[0][0] == maxim:
                    h_dict[k] = [maxim, sum(map(abs, v))]
                elif sp[0][0] < maxim:
                    h_dict = {k: [maxim, sum(map(abs, v))]}
            else:
                h_dict[k] = [maxim, sum(map(abs, v))]
        return list(h_dict.keys())[0]

    def __delitem__(self, key):
        del self[key]

    def det(self):
        """ Рекурсивный определитель """
        n, m = self.shape()
        assert n == m, 'Не квадратная'
        if n == 1:
            return self[0][0]
        if n == 2:
            return self[0][0] * self[1][1] - self[0][1] * self[1][0]

        line = self.__best_line()
        summa = 0
        for j, elem in enumerate(self[line]):
            if elem != 0:
                summa += ((-1) ** (j + line)) * Matrix.get_from_list(self.get_minor(self, i=line, j=j)).det() * elem
        return summa

    def swap_rows(self, i1: int, i2: int):
        """
        Меняет строки с индексами i1 и i2 местами
        :param i1: индекс 1-ой строки 
        :param i2: индекс 2-ой строки
        """
        self[i1], self[i2] = self[i2], self[i1]

    def divide_row_by_number(self, i, divider, j=0):
        """
        Деление i-ой строки на число divider начиная с j-го элемента
        :param i: индекс строки 
        :param divider: делитель строки
        :param j: индекс элемента строки с которого начинается(включительно) деление
        """
        assert divider != 0, 'Деление строки на ноль'
        for j in range(j, self.shape()[1]):
            self[i][j] /= divider

    def combine_rows(self, i1, i2, k, j=0):
        """
        Вычитание из i1-ой строки i2-ую строку умноженную на число k начиная с j-го элемента
        :param i1: индекс строки из которой вычитают
        :param i2: индекс вычитаемой строки
        :param k: множитель строки с индексом i2
        :param j: индекс элемента строки с которого начинается(включительно) вычитание
        """
        for j in range(j, self.shape()[1]):
            self[i1][j] -= k * self[i2][j]

    def get_index_max_elem_in_col(self, j=0, start=0, end=0):
        """
        получение индекса строки максимального элемента на j-ой позиции
        :param j: позиция макс. элемента 
        :return: индекс строки с макс. элементом на j-ой позиции
        """
        m, n = self.shape()
        assert 0 <= j <= n and 0 <= start <= end < m, 'Столбца с таким индеком не существует или указаны неверные границы'
        max_elem = 0
        for i in range(start, end + 1):
            elem = abs(self[i][j])
            if elem > max_elem:
                max_elem = elem
                index = i
        try:
            return index
        except:
            print(f'В {j} столбце все значения 0')

    def upper_triangular(self, swap_rows=False):
        """ приведение матрицы к верхней треугольной """
        m, n = self.shape()
        for i in range(m):
            # i совпадает с нужным j, так как идём поп диагонали
            if swap_rows:
                self.swap_rows(i, self.get_index_max_elem_in_col(j=i, start=i, end=m - 1))
            self.divide_row_by_number(i, self[i][i], j=i)
            # зануляем значения столбца под единицей
            for i2 in range(i, m - 1):
                self.combine_rows(i2 + 1, i, self[i2 + 1][i], j=i)

    def lower_triangular(self, swap_rows=False):
        """ приведение матрицы к верхней треугольной """
        m, n = self.shape()
        for i in range(m - 1, 0, -1):
            # i совпадает с нужным j, так как идём по диагонали
            if swap_rows:
                self.swap_rows(i, self.get_index_max_elem_in_col(j=i, start=0, end=i))
            self.divide_row_by_number(i, self[i][i])
            # зануляем значения столбца под единицей 
            for i2 in range(i):
                self.combine_rows(i2, i, self[i2][i])
        self.divide_row_by_number(0, self[0][0])

    def reverse_course(self):
        """ обратный ход (для Гаусса) применяется к верхним треугольным матрицам """
        m, n = self.shape()
        x_arr = [0] * m
        for i in range(m - 1, -1, -1):
            x_arr[i] = self[i][m] - sum(x * a for x, a in zip(x_arr[i + 1:m + 1], self[i][i + 1:m + 1]))
        return x_arr

    def solve_gauss(self):
        """ решение СЛАУ методом Гаусса"""
        if self.det() != 0:
            self.upper_triangular(swap_rows=True)  # приводим матрицу к верх.треугольной
            answer = self.reverse_course()  # делаем обратный ход и получаем ответы
            print(*(f"x{i + 1} = {elem}" for i, elem in enumerate(answer)), sep='\n')
            return answer
        else:
            print('Бесконечное кол-во решений')

    def solve_jordano_gauss(self):
        """ решение СЛАУ методом Жордана-Гаусса"""
        self.upper_triangular(swap_rows=True)
        self.lower_triangular()
        m = self.shape()[0]
        return [self[i][m] for i in range(m)]

    def norm_by_row(self):
        """
        Вычисление нормы по строке
        :return: норма по строке
        """
        m, n = self.shape()
        max_norm = 0
        for i in range(m):
            row_sum = 0
            for j in range(n):
                row_sum += abs(self[i][j])
            if row_sum > max_norm:
                max_norm = row_sum
        return max_norm

    def norm_by_col(self):
        """
        Вычисление нормы по столбцу
        :return: норма по столбцу
        """
        m, n = self.shape()
        max_norm = 0
        for j in range(n):
            col_sum = 0
            for i in range(m):
                col_sum += abs(self[i][j])
            if col_sum > max_norm:
                max_norm = col_sum
        return max_norm

    def norm_by_euclid(self):
        """
        Вычисление Евклидовой нормы (корень квадратный из суммы квадратов всех элементов матрицы)
        :return: Евклидова норма
        """
        m, n = self.shape()
        norm = 0
        for i in range(m):
            for j in range(n):
                norm += self[i][j] ** 2
        return norm ** (1 / 2)

    def __str__(self):
        string = ''
        for line in self:
            string += ', '.join([str(i) for i in line])
            string += '\n'
        return string

    def write_csv(self, path='./data/', file_name='result.csv', delimiter=' '):
        """ Запись матрицы в цсв """
        with open(path + file_name, 'w') as f:
            for row in self:
                print(delimiter.join(map(repr, row)), file=f)
        print('Матрица успешно записана!')

    @staticmethod
    def dot(first, second):
        """ Cкалярное умножение матриц """
        # считываем кол-во строк и столбцов матриц
        m1, n1 = first.shape()  # m - строки, n - столбцы
        m2, n2 = second.shape()
        assert n1 == m2, 'Неправильная размерность матриц'

        matrix = Matrix(m1, n2)
        for i in range(m1):  # кол-во строк первой
            for j in range(n2):  # кол-во столбцов второй
                summa = 0
                for index in range(n1):  # n1 == m2
                    summa += first[i][index] * second[index][j]
                matrix[i][j] = summa

        return matrix

    @staticmethod
    def unit(n):
        """ Создание единичной матрицы размером n на n """
        assert isinstance(n, int), 'Размерность задана не целочисленно'
        return Matrix.get_from_list([[1 if i == j else 0 for i in range(n)] for j in range(n)])

    @staticmethod
    def union(*args):
        """
        Объединение произвольного кол-ва Матриц по столбцам
        :param *args: экземпляры класса Matrix
        :return: объединённая матрица типа Matrix
        """
        assert len(args) != 0, 'Матрицы не были переданы'
        step = 0
        for matrix in args:
            assert isinstance(matrix, Matrix), 'Передан не экземпляр класса Matrix'
            new_m = matrix.shape()[0]
            if step == 0:
                old_m = new_m
                continue
            assert new_m == old_m, 'Размерность матриц по строкам не совпадает'
        return Matrix.get_from_list(
            [[elem for row in [matrix[i] for matrix in args] for elem in row] for i in range(old_m)])

    # =====================================Якоби===========================================
    @staticmethod
    def __diag_conv(self):
        '''
        Расстановка строк в правильном порядке
        (если диоганольность нарушена)
        '''
        a = []
        count = 0
        # Идея такая:  
        # В строке может быть только один Максимальный элемент
        # Мы его ищем и формируем список 
        # Если в списке совпадают найденные индексы, то мы 
        # возвращаем False
        for line in self:
            count += 1
            for index, elem in enumerate(line):
                if 2 * abs(elem) > sum(list(map(abs, line))):
                    a.append(index)
                    break

        if len(set(a)) == count:
            return a
        else:
            return False

    def method_jacoby(self, other, c):
        '''
        Сам Якоби
        Matrix.jacoby(other, c)
        other - Ответы (просто список)
        c - точность ( 1<c<0 )
        '''
        # Создаем нулевую обратную матрицу
        revers_matrix = [[0 for j in range(self.shape()[0])] for i in range(self.shape()[1])]
        indexes = Matrix().__diag_conv(self.matrix)  # То как надо переставить строки
        other = [i[0] for i in other]  # из списка списков делаем список
        if indexes:  # Если строки можно переставить в диоганально сильную матрицу
            solves = [1 for i in range(len(indexes))]  # Вектор ответов до
            new_sol = [0 for i in range(len(indexes))]  # Вектор ответов после
            count = 0
            while (max([abs(solves[i] - new_sol[i]) for i in range(len(indexes))]) > c) or (
                    count < 1000):  # Проверка на точность
                count += 1
                solves = new_sol.copy()  # Присваиваем старым зн. новые и пересчитываем
                # Встроенные работает быстрее переприсваивания 
                for key, val in enumerate(indexes):  # Мы должны из строк выражать разные переменны
                    summ = 0
                    for ind, elem in enumerate(self[key]):
                        if ind != val:
                            summ += ((-elem) * solves[ind]) / self[key][val]
                    new_sol[val] = other[key] / self[key][val] + summ  # Решение
                    # Подсчет обратной матрицы, тк в ней будет n Слау,
                    # Мы можем итеррироваться по n решениям Предыдущей СЛАУ
                    # Можно я не буду объснять как мы считаем слау по якоби?
                    # Единственное что, тут значения обновляются один за одним 
                    # А не векторами
                    for i in range(self.shape()[0]):
                        summ = 0
                        for ind, elem in enumerate(self[i]):
                            if ind != i:
                                summ += ((-elem) * revers_matrix[ind][key]) / self[i][i]
                        k = 1 if i == key else 0
                        revers_matrix[i][key] = k / self[i][i] + summ

            return [[i] for i in new_sol], Matrix.get_from_list(revers_matrix)
        else:
            return False

    def convert(self, type_):
        """
        Функция, которая конвертирует значения матрицы в переданный тип (int, float, complex, Fraction, ComplexFraction)
        меняет значения in-place
        :param type_: тип данных
        """
        n, m = self.shape()
        for i in range(n):
            for j in range(m):
                self[i][j] = type_.new_instance(self[i][j]) \
                    if type_ is Fraction or type_ is ComplexFraction \
                    else type_(self[i][j])

    # =========================Объединение алгоритмов==================================
    @staticmethod
    def solve(self, other, c, min_det=1e-11):
        """
        Функция решающая СЛАУ
        param:
            self - Матрица коэффициентов (тип Matrix)
            other - вектор свободных членов (тип list)
            c - точность
            min_det - минимальная величина определителя
        return - список ответов / False если их беск.много
        """
        if abs(self.det()) > min_det:
            jacoby = self.method_jacoby(other, c)
            if jacoby:
                answers, revers = jacoby
                if revers.norm_by_col() * self.norm_by_col() <= 100:  # число обусловленности для Якоби
                    print('Ответ: \n{}'.format(answers))
                    return answers
            else:
                print('Метод Якоби не работает\nДалее считаем по Жордано-Гауссу')
                # Объединяем матрицу коэффов, свободных членов и единичную (для обратной) и кидаем в Ж-Г
                main_lst = Matrix.union(self, Matrix.get_from_list(other), Matrix.unit(self.shape()[0]))
                answers = main_lst.solve_jordano_gauss()  # преобразуем main_list к диагонал
                # считываем обратную матрицу
                revers = [main_lst[i][len(self) + 1:] for i in range(len(main_lst))]
                # если число обусловленности выше 100 - переходим к дробям
                if Matrix.get_from_list(revers).norm_by_col() * self.norm_by_col() > 100:
                    main_lst = Matrix.union(self, Matrix.get_from_list(other), Matrix.unit(self.shape()[0]))
                    main_lst.convert(type_=Fraction)
                    answers = main_lst.solve_jordano_gauss()  # преобразуем main_list к диагонал
                    revers = [main_lst[i][len(self) + 1:] for i in range(len(main_lst))]
                    if Matrix.get_from_list(revers).norm_by_col() * self.norm_by_col() > 100:
                        print('Матрица слабообусловленная, выданные значения могут быть далеки от действительности')

            print(*(f"x{i + 1} = {elem}" for i, elem in enumerate(answers)), sep='\n')
            return answers
        print('скорее всего: бесконечное кол-во решений (матрица вырожденная)')
        return False

    @staticmethod
    def do_equation(equation: str):
        """ Считывание матричного уравнения и его решение """
        alph = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        arr_matrix = ''
        for i, elem in enumerate(equation):  # считываем вместо букв - матрицы
            if elem in alph and elem not in arr_matrix:
                arr_matrix += elem
                exec(f'{elem}=Matrix.get_by_console("{elem}")')
        try:
            return eval(equation)
        finally:
            return 'Посчитать не удалось'

    @staticmethod
    def get_by_console(name=''):
        """ Консольное считывание матрицы """
        m = int(input(f'Введите кол-во строк матрицы {name}:\n'))
        n = int(input(f'Введите кол-во столбцов матрицы {name}:\n'))
        matrix = Matrix(m, n)
        for i in range(m):
            for j in range(n):
                # пока принимаем только числа
                matrix[i][j] = float(input(f'Введите элемент {name.lower()}({i + 1}, {j + 1}):\n'))
        return matrix

    @staticmethod
    def read_csv(path='./data/', file_name='self.csv', delimiter=' '):
        """ Чтение матрицы из цсв """
        return Matrix.get_from_list(
            [[float(token) for token in line.split(delimiter)] for line in open(path + file_name)]
        )

    @staticmethod
    def write_matrix_to_csv(matrix, path='./data/', file_name='result.csv', delimiter=' '):
        """ Запись матрицы в цсв """
        with open(path + file_name, 'w') as f:
            for row in matrix:
                print(delimiter.join(map(repr, row)), file=f)
        print('Матрица успешно записана!')
