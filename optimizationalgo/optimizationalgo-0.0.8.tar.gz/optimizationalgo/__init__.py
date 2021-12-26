"""
``optimizationalgo``
=====================

Библиотека, реализующая оптимизационные алгоритмы для задач разного рода.
В данный момент поддерживаются алгоритмы для задачи коммовояжёра.
Для подробной информации пройдите в optimizationalgo.voyage

"""
from .voyage import simulated_annealing
from .voyage import ants_colony
from .voyage import create_visual

__author__ = 'Марк Козлов, Вячеслав Есаков, Артём Радайкин, Александр Савостьянов, Лев Памбухчян'

__version__ = "0.0.8"
