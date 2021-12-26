"""
DifferentialEquations
=====================

Библиотека, реализующая решение дифференциальных уравнений.
В данный момент поддерживаются алгоритмы: Эйлера, Эйлера Коши, Рунге-Кутты

"""

from .DiffEq import euler_method
from .DiffEq import euler_caushy
from .DiffEq import runge_kutta

__author__ = "Alexandr Savostianov"

__version__ = "0.0.1"