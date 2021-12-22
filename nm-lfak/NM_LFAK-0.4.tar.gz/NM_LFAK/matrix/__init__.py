from .Matrix import *
from .Fraction import *
from .ComplexFraction import *
from .SparseMatrix import *
from .Symbol import *


def get_eigen_values(matrix: Matrix, step=0.001, eps=0.001, iterations=1000000):
    """
    Функция для вычисления собственных значений матрицы на промежутке (-1000;1000)
    (только для действительного аргумента)
    :param matrix: матрица, для которой необходимо вычислить собственные значения
    :param step: шаг вычислений
    :param eps: число, значение меньше которого является нулем
    :param iterations: количество итерация для вычисления собственных значений
    :return: список собственных значений
    """
    lambda_ = Symbol()
    new_matrix = matrix - SparseMatrix.get_diag_matrix(matrix.n, matrix.m, lambda_)
    func = new_matrix.det().get_function('x')
    result = []
    for i in range(iterations):
        if abs(func(i * step)) < eps:
            result.append(i * step)
        if abs(func(-i * step)) < eps:
            result.append(-i * step)
    return result
