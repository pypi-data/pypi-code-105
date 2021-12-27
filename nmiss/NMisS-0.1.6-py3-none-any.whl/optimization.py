import pip

try:
    __import__('math')
except ImportError:
    pip.main([ 'install', 'math' ])

try:
    __import__('pandas')
except ImportError:
    pip.main([ 'install', 'pandas' ])

try:
    __import__('scipy')
except ImportError:
    pip.main([ 'install', 'scipy' ])

try:
    __import__('matplotlib')
except ImportError:
    pip.main([ 'install', 'matplotlib' ])

try:
    __import__('networkx')
except ImportError:
    pip.main([ 'install', 'networkx' ])

try:
    __import__('numpy')
except ImportError:
    pip.main([ 'install', 'numpy' ])

try:
    __import__('datetime')
except ImportError:
    pip.main([ 'install', 'datetime' ])


import math
import numpy as np
import pandas as pd
from scipy.stats import cauchy
import random
import matplotlib.pyplot as plt
import networkx as nx
from numpy.random import choice as np_choice

random_matrix = pd.DataFrame([[int(random.random() * 100) for _ in range(100)]
                              for _ in range(100)])
random_matrix.to_csv('random_matrix.csv', header=True, index=False)
random_matrix = pd.read_csv('random_matrix.csv')
spisok = random_matrix.values.tolist()


def simulated_annealing(dist, n, t0):
    """
    Функция, в которой реализован алгоритм имитации отжига
    :param dist: list -- матрица весов
    :param n: int -- длина пути
    :param t0: int -- оптимальная температура
    """

    def temperatura(k, t):
        """
        Функция расчета оптимальной температуры для алгоритма имитации отжига
        :param k: int -- количество городов
        :param t: int -- температура
        :return t/k: float -- коэффициент,
        который нужен для вычисления следующей температуры
        """
        return t / k

    way = [element for element in range(n)]
    rand0 = [element for element in range(1, n)]
    tk = 1
    m = 1
    s = 0
    x0 = 0.1
    x = [x0]
    t = t0
    s_list = []
    while t > tk:
        sp = 0
        t = temperatura(m, t0)
        x.append(random.uniform(0, 1))
        way_p = [way[j] for j in range(n)]
        rand = random.sample(rand0, 2)
        way_p[rand[0]], way_p[rand[1]] = way_p[rand[1]], way_p[rand[0]]
        for j in range(n - 1):
            sp = sp + dist[way_p[j]][way_p[j + 1]]
        sp = sp + dist[way_p[0]][way_p[-1]]
        if m == 1 or sp < s:
            s = sp
            way = [way_p[j] for j in range(n)]
        else:
            p = math.exp(-(sp - s) / t)
            if x[m - 1] < p:
                x[m - 1], x[m] = x[m], x[m - 1]
                s = sp
                way = [way_p[j] for j in range(n)]
        m += 1
        s_list.append(s)
    way.append(way[0])
    return way, s, m, s_list


def inlet():
    """
    Функция ввода и выбора, каким путем мы хотим задать матрицу весов
    :return dist: list -- матрица весов
    """

    def file():
        """
        Функция, которая считывает файл csv и заполняет матрицу
        значениями, взятыми оттуда
        :return matrix_1: list -- матрица, считываемая с csv файла
        """
        import csv
        matrix_1 = []
        name = input("Введите названи файла. Например, city.csv: ")
        with open(name) as file:
            reader = csv.reader(file, delimiter=';', quotechar=',')
            for row in reader:
                matrix_1.append(row)
        matrix_1 = [[float(matrix_1[i][j]) for j in range(len(matrix_1))]
                    for i in range(len(matrix_1))]
        return matrix_1

    def random_dist(k):
        """
        Функция, которая герерирует матрицу
        :param k: int -- количество городов
        :return d: list -- сгенерируемая матрица
        """
        d = [[0 if elem == j else random.uniform(0, 10) for j in range(k)]
             for elem in range(k)]
        for elem in range(k):
            print(d[elem])
        return d

    def matr(m, n):
        """
        Функция заполнения матрицы элементов.
        :param m: int -- количество строк в матрице
        :param n: int -- количество столбцов в матрице
        :return matrix: list -- заполненная элементами матрица
        """

        def el_int(el):
            """
            Функция на проверку типа введенного элемента в матрице (целое).
            Она возвращает True, если число целое, False - если нет.
            :param el: элемент матрицы
            """
            try:
                int(el)
                return True
            except ValueError:
                return False

        def el_float(el):
            """
            Функция на проверку типа введенного элемента в матрице (вещественное).
            Она возвращает True, если число вещественное, False - если нет.
            :param el: элемент матрицы
            """
            try:
                float(el)
                return True
            except ValueError:
                return False

        def el_complex(el):
            """
            Функция на проверку типа введенного элемента в матрице (комплексное).
            Она возвращает True, если число комплексное, False - если нет.
            :param el: элемент матрицы
            """
            try:
                complex(el)
                return True
            except ValueError:
                return False

        def rev_complex(h):
            """
            Функция преобразует комплексное число в нормальный вид, т. е. в вид a + i*b
            Пример: если вы ввели -j + 1, функция преобразует это в 1 - j
            :param h: str -- элемент матрицы
            :return h_rev: str -- преобразованный элемент
            """
            h_rev = ''
            sep = 0
            if h[0] == '+' or h[0] == '-':
                for element_matr in range(1, len(h)):
                    if h[element_matr] == '+' or h[element_matr] == '-':
                        sep = element_matr
                        break
                h_rev = h[sep:len(h)] + h[0:sep]
            else:
                for element_matr in range(0, len(h)):
                    if h[element_matr] == '+' or h[element_matr] == '-':
                        sep = element_matr
                        break
                h_rev = h[sep:len(h)] + '+' + h[0:sep]
            return (h_rev)

        matrix = []
        print('Введите элементы строки матрицы через пробел:')
        for elem_matr in range(0, m):
            a = []
            row = input()
            row = row.split(' ')
            matrix.append(row)
            if len(row) != n:
                print('Некорректное количество элементов в строке матрицы.')
                exit()
            for j in range(0, n):
                el = matrix[elem_matr][j]
                k = 0
                while k == 0:
                    if el_int(el) is True:
                        matrix[elem_matr][j] = int(el)
                        k = 1
                    else:
                        if el_float(el) is True:
                            matrix[elem_matr][j] = float(el)
                            k = 1
                        else:
                            if el_complex(el) is True:
                                matrix[elem_matr][j] = complex(el)
                                k = 1
                            else:
                                if el_complex(rev_complex(el)) is True:
                                    matrix[elem_matr][j] = complex(
                                        rev_complex(el))
                                    k = 1
                                else:
                                    el = input('Неверный формат ввода. '
                                               'Повторите ввод '
                                               'элемента [{}, '
                                               '{}]: '.format(elem_matr, j))
        return (matrix)

    print("Ввод данных")
    length = int(input("Введите: 1 - для считывания файла с устройства, "
                       "2 - для случайной генерации, "
                       "3 - для ввода матрицы с клавиатуры\n"))
    if length == 1:
        dist = file()
    if length == 2:
        k = int(input("Введите количество городов: "))
        dist = random_dist(k)
    if length == 3:
        k = int(input("Введите количество городов: "))
        dist = matr(k, k)
    return dist


class AntColony(object):
    """
    Класс для нахождения оптимального пути алгоритмом Муравьиной колонии.
    """

    def __init__(self, distances, n_ants, n_best, n_iterations,
                 decay, alpha=1, beta=1):
        """
        Функция для замены 0 на inf
        :param distances: list -- матрица весов
        :param n_ants: int -- количество муравьев
        :param n_best: int
        :param n_iterations: int -- количество итераций
        :param decay: float
        :param alpha: int -- значение ориентации феромонов
        :param beta: int -- значение ориентации на длину пути
        """
        i = 0
        j = 0
        while i < len(distances):
            while j < len(distances):
                if distances[i][j] == 0:
                    distances[i][j] = np.inf
                    i += 1
                    j += 1
                else:
                    continue

        self.distances = np.array(distances)
        self.pheromone = np.ones(self.distances.shape) / len(self.distances)
        self.all_inds = range(len(self.distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        """
        Функция для нахождения лучшего пути и его стоимости
        :return all_time_shortest_path: tuple -- кортеж, в котором список
        корттежей лучшего пути и его стоимость
        """
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        for elem in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            self.spread_pheronome(all_paths, self.n_best,
                                  shortest_path=shortest_path)
            shortest_path = min(all_paths, key=lambda x: x[1])
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path
            self.pheromone * self.decay
        return all_time_shortest_path

    def spread_pheronome(self, all_paths, n_best, shortest_path):
        """
        Функция для нахождения оптимального значения феромона
        :param all_paths: list -- список кортежей пути и их стоимости
        :param n_best: int
        :param shortest_path: tuple -- кортеж, в котором список кортежей
        пути и их стоимость
        """
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move] += 1.0 / self.distances[move]

    def gen_path_dist(self, path):
        """
        Функция для расчета стоимости пути
        :param path: list -- список кортежей пути
        :return total_dist: numpy.float64 --  стоимость  пути
        """
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele]
        return total_dist

    def gen_all_paths(self):
        """
        Функция, в которой в список добавляются кортежи путей и их стоимость
        :return all_path: list -- список кортежей пути и их стоимости
        """
        all_paths = []
        for elem in range(self.n_ants):
            path = self.gen_path(0)
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_all_cost(self):
        """
        Функция для расчета стоимости каждого пути
        :return cost: list -- список стоимости каждого пути
        """
        cost = []
        for elem in range(self.n_ants):
            path = self.gen_path(0)
            cost_1 = self.gen_path_dist(path)
            cost.append(cost_1.tolist())
        return cost

    def gen_path(self, start):
        """
        Функция для расчета пути
        :param start: int -- начальная вершина
        :return path: list -- список кортежей пути
        """

        path = []
        visited = set()
        visited.add(start)
        prev = start
        for elem in range(len(self.distances) - 1):
            move = self.pick_move(self.pheromone[prev], self.distances[prev],
                                  visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start))
        return path

    def pick_move(self, pheromone, dist, visited):
        """
        Функция для нахождения вершин, в которых путь оптимален
        :param pheromone: numpy.ndarray -- феромон, который необходим для
        поиска лучшего пути
        :param dist: list -- матрица весов
        :param visited: set -- множество посещенных вершин
        :return move: numpy.int64 -- вершины пути
        """
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0
        row = pheromone ** self.alpha * ((1.0 / dist) ** self.beta)
        norm_row = row / row.sum()
        move = np_choice(self.all_inds, 1, p=norm_row)[0]
        return move


def route_conversion(lst):
    """
    Функция для получения лучшего пути в формате 0-2-1-0
    :param lst: list -- список кортежей лучшего пути
    :return '-'.join(result): numpy.float64 -- лучший путь в формате 0-1-2-0
    """
    result = []
    for elem in range(len(lst)):
        if elem == 0:
            result.append('-'.join([str(lst[elem][0]), str(lst[elem][1])]))
        else:
            result.append(str(lst[elem][1]))
    return '-'.join(result)


def route_con(lst):
    """
    Функция для получения списка лучшего пути
    :param lst: list -- список кортежей лучшего пути
    :return result: list -- список лучшего пути
    """
    result = []
    for elem in range(len(lst)):
        if elem == 0:
            result.append(lst[elem][0])
            result.append(lst[elem][1])
        else:
            result.append(lst[elem][1])
    return result


def graph(n, way, dist):
    """
    Функция для построения графа алгоритма Имитации отжига
    :param n: int -- длина пути
    :param way: list -- полученный самый оптимальный путь
    :param dist: list -- матрица весов
    """
    rand = [i for i in range(n)]
    g = nx.Graph()
    g.add_nodes_from(rand)
    for elem in range(n):
        for j in range(elem + 1, n):
            if dist[elem][j] != 0:
                g.add_edge(rand[elem], rand[j])
    comb = []
    for elem in range(n):
        if rand.index(way[elem]) > rand.index(way[elem + 1]):
            comb.append(tuple([way[elem + 1], way[elem]]))
        else:
            comb.append(tuple([way[elem], way[elem + 1]]))
    edge_colors = ["red" if elem in comb else "blue" for elem in g.edges()]
    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(g)
    nx.draw_networkx(g, pos, edge_color=edge_colors)
    plt.title("Алгоритм Отжига")
    plt.show()


def graph_1(n, way, dist):
    """
    Функция для построения графа алгоритма Муравьиной колонии
    :param n: int -- длина пути
    :param way: list -- полученный самый оптимальный путь
    :param dist: list -- матрица весов
    """
    rand = [_ for _ in range(n)]
    g = nx.Graph()
    g.add_nodes_from(rand)
    for elem in range(n):
        for j in range(elem + 1, n):
            if dist[elem][j] != 0:
                g.add_edge(rand[elem], rand[j])
    comb = []
    for elem in range(n):
        if rand.index(way[elem]) > rand.index(way[elem + 1]):
            comb.append(tuple([way[elem + 1], way[elem]]))
        else:
            comb.append(tuple([way[elem], way[elem + 1]]))
    edge_colors = ["red" if elem in comb else "blue" for elem in g.edges()]
    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(g)
    nx.draw_networkx(g, pos, edge_color=edge_colors)
    plt.title("Алгоритм Муравьиной Колонии")
    plt.show()

def runoptimisationscript():
    """
    Функция для запуска итерационного цикла (показа работы самих программ оптимищации)
    :return:
    """
    distant = inlet()
    len_m = len(distant)
    temper = len_m ** 2
    w, s, q, s_list = simulated_annealing(distant, len_m, temper)
    print("Длина маршрута: ", s)
    print("Маршрут алгоритма имитации отжига: ", w)
    print("Количество итераций в маршруте имитации отжига: ", q)
    graph(len_m, w, distant)

    distance = distant
    ant_colony = AntColony(distance, len(distance) * 2, 5, len(distance) * 4,
                           0.95, alpha=1, beta=1)
    shortest_path = ant_colony.run()
    c = ant_colony.gen_all_cost()
    route = shortest_path[0]
    len_m = len(distance)
    results = route_con(shortest_path[0])
    print("Полученный путь алгоритмом муравьиной колонии:",
          route_conversion(shortest_path[0]))
    print("Стоимость пути муравьиной колонии:", shortest_path[1])
    graph_1(len_m, results, distance)

    plt.subplot(2, 1, 1)
    plt.plot(s_list)
    plt.title('Алгоритм отжига')
    plt.xlabel('Номер итерации')
    plt.ylabel('Длина маршрута')
    plt.subplot(2, 1, 2)
    plt.plot(c)
    plt.title('Алгоритм Муравьиной колонии')
    plt.xlabel('Номер итерации')
    plt.ylabel('Длина маршрута')
    plt.show()