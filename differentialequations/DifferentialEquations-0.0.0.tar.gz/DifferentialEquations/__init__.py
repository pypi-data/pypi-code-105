"""
DifferentialEquations
=====================

Библиотека, реализующая решение дифференциальных уравнений.
В данный момент поддерживаются алгоритмы: Эйлера, Эйлера Коши, Рунге-Кутты

"""

__all__ = ['euler_method', 'euler_caushy', 'runge_kutta']

from .Euler import euler_method
from .Euler_Caushy import euler_caushy
from .Runge_Kutta import runge_kutta

__author__ = "Alexandr Savostianov"

__version__ = "0.0.0"