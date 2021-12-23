import csv
import numpy as np
from numba import prange
import networkx as nx
import matplotlib.pyplot as plt
from functools import reduce


def collect_nodes(points, highlighted_nodes=[], color='#79FF06', highlighted_color='blue', width=200, highlighted_width=400):
    """
    Собирает необходимые нам вершины в нужный формат

    Parameters
    ----------
    points : [str, str, ...]
        Вершины графа.
    highlighted_nodes : [str, str, ...], optional
        Выделенные вершины графа. 
        По умолчанию [].
    color : str, optional
        Цвет обычных вершин. 
        По умолчанию '#79FF06'.
    highlighted_color : str, optional
        Цвет выделенных вершин. 
        По умолчанию 'blue'.
    width : int, optional
        Ширина обычных вершин. 
        По умолчанию 200.
    highlighted_width : int, optional
        Ширина выделенных вершин. 
        По умолчанию 400.

    Returns
    -------
    result : [(str, {'color': str, 'width': int}),
              (str, {'color': str, 'width': int}),
              ...]
        Список вершин с их параметрами.

    """
    result = []
    for p in points:
        if p in highlighted_nodes:
            result.append((p, {"color": highlighted_color, "width": highlighted_width}))
        else:
            result.append((p, {"color": color, "width": width}))
    return result
    

def draw_graph(points, labels, dict_labels, highlighted_nodes=[], with_labels=False, with_label_labels=False):
    """
    Функция, рисующая заданный граф

    Parameters
    ----------
    points : [str, str, ...]
        Вершины графа.
    labels : [(str, str, int, str),
              (str, str, int, str),
              ...]
        Список кортежей из рёбер типа (<Вершина1>, <Вершина2>, <Вес ребра>, <Цвет ребра>).
    dict_labels : {(str, str): int,
                   (str, str): int,
                   ...}
        Словарь рёбер с их весами.
    highlighted_nodes : [str, str, ...], optional
        Выделенные вершины графа. 
        По умолчанию [].
    with_labels : bool, optional
        Для вывода весов рёбер. 
        По умолчанию False.
    with_label_labels : bool, optional
        Для вывода названий вершин. 
        По умолчанию False.

    """
    
    graph = nx.Graph()
    args_points = collect_nodes(points, highlighted_nodes)
    graph.add_nodes_from(args_points)
    for label in labels:
        if label[3] == 'red':
            graph.add_edge(label[0],
                       label[1],
                       color=label[3],
                       weight=label[2],
                       width=7)
        else:
            graph.add_edge(label[0],
                       label[1],
                       color=label[3],
                       weight=label[2],
                       width=3)
    pos = nx.kamada_kawai_layout(graph)
    edges = graph.edges()
    nodes = graph.nodes
    node_colors = [graph.nodes[n]['color'] for n in nodes]
    node_widths = [graph.nodes[n]['width'] for n in nodes]
    colors = [graph[e[0]][e[1]]['color'] for e in edges]
    widths = [graph[e[0]][e[1]]['width'] for e in edges]
    plt.figure(1,figsize=(10,10))
    nx.draw(graph, pos, edgelist=edges, edge_color=colors, node_color=node_colors, with_labels=with_labels, width=widths, node_size=node_widths)
    if with_label_labels:
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=dict_labels)
    plt.show()

def transfer_labels(matrix, shortest_path, color='black', highlighted_color='red'):
    """
    Переводит матрицу весовых коэфициентов в список рёбер и вершин с их аттрибутами

    Parameters
    ----------
    matrix : [[float, float, ...],
              [float, float, ...],
              ...]
        Матрица весовых коэфициентов.
    shortest_path : [(str, str), (str, str), ...]
        Список из всех ребёр, формирующих кратчайший путь.
    color : str, optional
        Цвет обычных рёбер. 
        По умолчанию 'black'.
    highlighted_color : str, optional
        Цвет выделенных рёбер (из списка кратчайшего пути). 
        По умолчанию 'red'.

    Returns
    -------
    points : [str, str, ...]
        Вершины графа.
    labels : [(str, str, int, str),
              (str, str, int, str),
              ...]
        Список кортежей из рёбер типа (<Вершина1>, <Вершина2>, <Вес ребра>, <Цвет ребра>).
    dict_labels : {(str, str): int,
                   (str, str): int,
                   ...}
        Словарь рёбер с их весами.

    """
    labels = []
    dict_labels = {}
    points = [str(x) for x in range(len(matrix))]
    for i in range(len(matrix) - 1):
        for j in range(i + 1, len(matrix)):
            if tuple([i, j]) in shortest_path or tuple([j, i]) in shortest_path:
                labels.append((str(i), str(j), matrix[i, j], highlighted_color))
                labels.append((str(j), str(i), matrix[j, i], highlighted_color))
            else:
                labels.append((str(i), str(j), matrix[i, j], color))
                labels.append((str(j), str(i), matrix[j, i], color))
            dict_labels[(str(i), str(j))] = matrix[i, j]
            dict_labels[(str(j), str(i))] = matrix[j, i]
    return points, labels, dict_labels

def get_matrix():
    """
    Функция считывания или генерирования матрицы весовых коэффициентов

    Returns
    -------
    matrix : [[float, float, ...],
              [float, float, ...],
              ...]
        Матрица весовых коэфициентов.

    """
    while True:
        ans = input('Как вы хотите ввести матрицу весовых коэффициентов?\n 1. csv файл\n 2. Рандомная генерация\n 3. Ручной ввод (не рекомендуется при большом кол-ве вершин в графе)\n ->')
        if ans in ['1', '2', '3']:
            break
        print('Вы ввели не верный вариант, выберите пожалуйста из вариантов 1/2/3')

    if ans == '1':
        while True:
            filename = input('Введите название файла .csv\n ->')
            try:
                with open(filename, 'r') as file:
                    pass
            except FileNotFoundError:
                print('Такой файл не найден, попробуйте еще раз')
                continue
            if filename.endswith('.csv'):
                break
            print('Вы ввели файл с отличным от .csv расширением, попробуйте еще раз')


        with open(filename, 'r') as file:
            matrix = []
            data = csv.reader(file)
            for row in data:
                matrix.append([float(element) for element in row])
            matrix = np.array(matrix)
    elif ans == '2':
        n = int(input('Введите кол-во городов (вершин)\n ->'))
        matrix = np.zeros((n, n), float)
        np.fill_diagonal(matrix, float('inf'))
        for i in range(n - 1):
            for j in range(i + 1, n):
                value = round(np.random.uniform() * (n - 1) + 1, 3)
                matrix[i][j] = value
                matrix[j][i] = value
    else:
        n = int(input('Введите кол-во городов (вершин)\n ->'))
        matrix = np.zeros((n, n), float)
        np.fill_diagonal(matrix, float('inf'))
        for i in range(n - 1):
            for j in range(i + 1, n):
                value = float(input(f'Введите длину дороги (вес ребра) между городами {i} и {j}: '))
                matrix[i][j] = value
                matrix[j][i] = value
    return matrix, len(matrix)


def ant_colony_algoritm(distances, decay=0.95, alpha=1, beta=1, epsilon=0.001):
    """
    Оптимизация методом имитации муравьиной колонии

    Parameters
    ----------
    distances : [[float, float, ...],
              [float, float, ...],
              ...]
        Матрица весовых коэфициентов.
    decay : float, optional
        Коэф выветривания феромонов. Строго меньше 1.
        По умолчанию 0.95.
    alpha : int, optional
        Коэф. значимости феромонов. 
        По умолчанию 1.
    beta : int, optional
        Коэф значимости растояния. 
        По умолчанию 1.
    epsilon : float, optional
        Точность вычисления. Рекомендуется брать малые значения
        По умолчанию 0.001.

    Returns
    -------
    all_time_shortest_path : ((str, str),
                              (str, str),
                              ...,
                              int)
        Кортеж из рёбер, составлящий кратчайший путь и вес этого пути.
    n_iterations : int
        Кол-во иттераций, потребовавшихся для завершения работы.
    paths_list : [float, float, ...]
        Список всех изменений веса кратчайшего пути за время работы программы.

    """
    
    def gen_all_paths():
        all_paths = []
        for i in prange(n_ants):
            path = gen_path(i)
            all_paths.append((path, gen_path_dist(path)))
        return all_paths
    
    def gen_path_dist(path):
        total_dist = 0
        for ele in path:
            total_dist += distances[ele]
        return total_dist
    
    def gen_path(start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for i in prange(len(distances) - 1):
            move = pick_move(pheromone[prev], distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start))   
        return path
    
    def pick_move(pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0

        row = pheromone ** alpha * (( 1.0 / dist) ** beta)

        norm_row = row / row.sum()
        move = np.random.choice(all_inds, 1, p=norm_row)[0]
        return move
    
    def spread_pheronome(all_paths):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths:
            for move in path:
                pheromone[move] += 1.0 / distances[move]

    n_ants=len(distances)
    n_iterations=len(distances) ** 2 // 10
    pheromone = np.ones(distances.shape) / len(distances)
    all_inds = range(len(distances))
    shortest_path = None
    all_time_shortest_path = ("", np.inf)
    same_count = 0
    paths_list = []
    for i in prange(n_iterations):
        all_paths = gen_all_paths()
        spread_pheronome(all_paths)
        shortest_path = min(all_paths, key=lambda x: x[1])
        if shortest_path[1] == all_time_shortest_path[1]:
            same_count += 1
        else:
            same_count = 0
        if shortest_path[1] < all_time_shortest_path[1]:
            all_time_shortest_path = shortest_path 
        paths_list.append(all_time_shortest_path[1])
        if same_count == 5:
            break
        pheromone = pheromone * decay
    return all_time_shortest_path, n_iterations, paths_list


def otjig(matrix, t_min=0.5, t_max=1000):
    """
    Алгоритм оптимизации имитацией отжига

    Parameters
    ----------
    matrix : [[float, float, ...],
              [float, float, ...],
              ...]
        Матрица весовых коэфициентов.
    t_min : float, optional
        Минимальная температура. 
        По умолчанию 0.5.
    t_max : float, optional
        Максимальная температура. 
        По умолчанию 1000.

    Returns
    -------
    result : ((str, str),
                              (str, str),
                              ...,
                              int)
        Кортеж из рёбер, составлящий кратчайший путь и вес этого пути.
    count : int
        Кол-во иттераций, потребовавшихся для завершения работы.
    paths_list : [float, float, ...]
        Список всех изменений веса кратчайшего пути за время работы программы.

    """
    n = len(matrix)
    T_0 = np.array(np.linspace(0, n-1, n), int)
    np.random.shuffle(T_0)
    v = sum([matrix[T_0[i-1]][T_0[i]] for i in range(len(T_0))])
    temp = t_max
    iteration = 0
    count = 0
    paths_list = []
    while temp > t_min:
        count += 1
        i, j = sorted(np.random.choice(np.array(np.linspace(1, n-1, n-1), int),  size=2, replace=False))
        T = T_0.copy()
        T[i:j+1] = T[j:i-1:-1]
        v_new = sum([matrix[T[k-1]][T[k]] for k in range(len(T))])
        paths_list.append(v)
        if v_new < v:
            iteration += 1
            v = v_new
            T_0 = T
            temp = t_max / iteration
        elif v < v_new:
            if np.random.uniform() <= np.exp(-(v_new - v)/temp):
                iteration += 1
                v = v_new
                T_0 = T
                temp = t_max / iteration
    result = []
    for i in range(len(T_0)):
        result.append((T_0[i - 1], T_0[i]))     
                
    return (result, v), count, paths_list