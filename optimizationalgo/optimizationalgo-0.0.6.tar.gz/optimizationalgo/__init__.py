"""
``optimizationalgo.voyage``
===========================

Модуль, реализующий оптимизационные алгоритмы решения задачи коммивояжёра.
Представлены следующие алгоритмы: имитация муравьиной колонии и симуляция отжига.

"""
from .voyage import simulated_annealing
from .voyage import ants_colony

__author__ = 'Mark Kozlov'

try:
    from .version import version
except ImportError:
    version = "0.0.1"

__version__ = version
