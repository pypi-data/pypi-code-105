# Импорты

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.fft import fft,fftfreq
from pywt import *
from pylab import *
import csv
from datetime import datetime
from google.colab import files


def Read_csv(filename):
    random_matrix = pd.read_csv(filename)
    spisok = random_matrix.values.tolist()
    return spisok


def make_plots(x, y, label, color, linewidth=2):  # функция для графика синусоиды или частотного спектра
    """
    Отдельная функция для построения графика (с определенным форматом легенды, чтобы можно было помногу раз обращаться в программе)
      Входные параметры:
        y: list - список из Y-значений
        x: list - список из X-значений
        label: str - надпись на графике
        color: str - цвет линии графика
        linewidth: int - толщина линии графика
    """
    plot(x, y, color=color, linewidth=linewidth, label=label)
    legend(loc='upper right')


def make_plots_wavelet(x, approx, decomp, filename):  # функция для графика декомпозиций
    """
    Построение апроксимирующей функции для вейвлет-декомпозиций 0 и 4 уровней, а также самих вейвлетов
      Входные параметры:
        x: list - список из X-значений
        approx: list - список из вложенных списков Y-значений для апроксимаций и вейвлетов
        decomp: int - уровень декомпозиции
        filename: str - название файла (выводится в легенде)
    """
    l = 'upper right'
    fig = plt.figure(figsize=(10, 7))
    ax = plt.subplot(111)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.2, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    subplot(decomp + 4, 1, 1)
    make_plots(x, y, label='Входные данные', color='g')
    subplot(decomp + 4, 1, 2)
    plot(approx[0][0], color='red', linewidth=3, label='Аппроксимирующая функция 0')
    subplot(decomp + 4, 1, 3)

    plot(approx[4][0], color='red', linewidth=3, label='Аппроксимирующая функция 4')
    for i in range(decomp):
        subplot(decomp + 4, 1, i + 4)
        if (i == decomp):
            linewidth, color = 3, 'b'
        plot(approx[i + 1][1][10:-10], label='Вейвлет декомпозиция ' + str(i + 1) + ' уровня')
        legend(loc=l)

    plt.gcf().set_size_inches(18, 11)


def Read_csv_real(filename):  # Считывание реальной выборки
    """
    Отдельная функция для считывания файла с валютой (потому что там данные записаны
    совершенно по-другому нежели чем в файлах с выборкой от преподавателя)

      Входные параметры:
        filename: str - имя файла

      Выходные параметры:
        spisok: list - список из вложенных списков значений X и Y
    """
    with open(filename, encoding='unicode_escape') as csv_file:
        file_reader = csv.DictReader(csv_file)
        y = []
        spisok = []
        for col in file_reader:
            float_part = (list(col.values())[1])[0].split(';')[0]
            l = float((list(col.values())[0]).split(';')[2] + '.' + float_part)
            y.append(l)
    x = list(np.linspace(start=1, stop=len(y), num=len(y)))
    spisok.append(x)
    spisok.append(list(reversed(y)))
    return spisok