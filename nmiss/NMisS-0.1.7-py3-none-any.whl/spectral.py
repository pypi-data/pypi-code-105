# Импорты

import pip

try:
    __import__('matplotlib')
except ImportError:
    pip.main([ 'install', 'matplotlib' ])

try:
    __import__('pandas')
except ImportError:
    pip.main([ 'install', 'pandas' ])

try:
    __import__('numpy')
except ImportError:
    pip.main([ 'install', 'numpy' ])

try:
    __import__('scipy')
except ImportError:
    pip.main([ 'install', 'scipy' ])

try:
    __import__('pywt')
except ImportError:
    pip.main([ 'install', 'pywt' ])

try:
    __import__('pylab')
except ImportError:
    pip.main([ 'install', 'pylab' ])

try:
    __import__('csv')
except ImportError:
    pip.main([ 'install', 'csv' ])

try:
    __import__('datetime')
except ImportError:
    pip.main([ 'install', 'datetime' ])


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.fft import fft,fftfreq
import pywt
import pylab
import csv
from datetime import datetime



def Read_csv(filename):
    random_matrix = pd.read_csv(filename)
    spisok = random_matrix.values.tolist()
    return spisok

# Расчет коэффициентов несинусоидальности
def non_sin_coefficient_wavelet(wav,y):
    di  = [np.std(pywt.wavedec(y, wav, level=i+1)[1])**2 for i in range(4)]
    a4 = np.std(pywt.wavedec(y, wav, 4)[0])
    return sum(di)**0.5/a4

def non_sin_coefficient_Furie(y):
   S_0 = max(y)
   S_secondary = sum([i for i in y if i!=S_0])
   return S_secondary/S_0

# функция для дисперсии
def dispersion(f,f_i):
  s = sum([(f[i]-f_i[i])**2 for i in range(len(f))])
  return s**0.5

def make_plots(x, y, label, color, linewidth=2):  # функция для графика синусоиды или частотного спектра
    """
         Отдельная функция для построения графика (с определенным форматом легенды, чтобы можно было помногу раз обращаться в программе)

         :params label: str - надпись на графике

         :params y: list - список из Y-значений

         :params x: list - список из X-значений

         :params color: str - цвет линии графика

         :params linewidth: int - толщина линии графика

         :return spisok: list - список из вложенных списков значений X и Y
    """
    plt.plot(x, y, color=color, linewidth=linewidth, label=label)
    plt.legend(loc='upper right')


def make_plots_wavelet(x, y, approx, decomp, filename):  # функция для графика декомпозиций
    """
         Построение апроксимирующей функции для вейвлет-декомпозиций 0 и 4 уровней, а также самих вейвлетов

         :params approx: list - список из вложенных списков Y-значений для апроксимаций и вейвлетов

         :params decomp: int - уровень декомпозиции

         :params x: list - список из X-значений

         :params y: list - список из Y-значений

         :params filename: str - имя файла

         :return spisok: list - список из вложенных списков значений X и Y
    """
    l = 'upper right'
    fig = plt.figure(figsize=(10, 7))
    ax = plt.subplot(111)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.2, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.subplot(decomp + 4, 1, 1)
    make_plots(x, y, label='Входные данные', color='g')
    plt.subplot(decomp + 4, 1, 2)
    plt.plot(approx[0][0], color='red', linewidth=3, label='Аппроксимирующая функция 0')
    plt.subplot(decomp + 4, 1, 3)

    plt.plot(approx[4][0], color='red', linewidth=3, label='Аппроксимирующая функция 4')
    for i in range(decomp):
        plt.subplot(decomp + 4, 1, i + 4)
        if (i == decomp):
            linewidth, color = 3, 'b'
        plt.plot(approx[i + 1][1][10:-10], label='Вейвлет декомпозиция ' + str(i + 1) + ' уровня')
        plt.legend(loc=l)

    plt.gcf().set_size_inches(18, 11)


def Read_csv_real(filename):  # Считывание реальной выборки
    """
         Отдельная функция для считывания файла с валютой (потому что там данные записаны
         совершенно по-другому нежели чем в файлах с выборкой от преподавателя)

         :params filename: str - имя файла

         :return spisok: list - список из вложенных списков значений X и Y
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

def Frequency_spectrum(x: list, y: list, filename: str):
    """
         Рассчет и построение амплитудно-частотной характеристики сигнала (какой сигнал встречается чаще всего)
         :params x: list - X-значения

         :params y: list - Y-значения

         :params filename: str - имя файла
    """
    yf = pylab.fft(y)  # быстрое преобразование Фурье
    period = len(y) * 0.1  # Период
    xf = pylab.fftfreq(len(y), 1 / period)
    plt.Figure(figsize=(20, 20))
    plt.subplot(1, 3, 1)
    make_plots(x, y, filename, 'b', 1)  # выводим график исходной функции
    plt.subplot(1, 3, 2)
    plt.bar(xf, np.abs(yf) * 0.0025, align='center', label='Частотный спектр', color='red')  # Гистограмма
    plt.legend(loc='upper right')
    plt.xlim(-20, 20)
    plt.subplot(1, 3, 3)
    y_i = pylab.ifft(yf)  # восстанавливаем исходный сигнал
    make_plots(x, y_i, label='Восстановленный сигнал', color='g')  # частотный спектр
    plt.gcf().set_size_inches(30, 10)
    print('Коэффициент несинусоидальности в комплексной форме:', non_sin_coefficient_Furie((yf)), '\n')
    print('Коэффициент несинусоидальности с np.abs():', non_sin_coefficient_Furie((np.abs(yf))), '\n')
    print('Дисперсия:', dispersion(np.abs(y_i), y))  # вычисляем дисперсию


def Wavelet_function(x: list, y: list, decomp: int, name: str, filename: str):
    """
         Функция считает апроксимации и вейвлет-декомпозиции уровней от 1 до 4. Построение вейвлетов - то же самое, что и АХЧ,
         но с зависимостью от времени, показывает частоту сигнала в определенный момент времени
         :params x: list - X-значения

         :params y: list - Y-значения

         :params name: str - название вейвлета

         :params decomp: int - уровень декомпозиции

         :params filename: str - имя файла
    """
    approx = [ pywt.wavedec(y, name, level=i) for i in range(decomp + 1) ]
    make_plots_wavelet(x, y, approx, decomp, filename)

def Approximation_Comparison(x: list, y: list, decomp: int, filename: str):
    """
         Функция считает и выводи апроксимации для функций на основе X,Y значений и декомпозиции
         :params x: list - X-значения

         :params y: list - Y-значения

         :params decomp: int - уровень декомпозиции

         :params filename: str - имя файла
    """
    plt.figure(figsize=(10, 7))
    names = {'sym6': 'Гаусс', 'haar': 'Хаар', 'bior4.4': 'Мексиканская шляпа', 'db2': 'Добеши'}
    colors = [ 'r', 'b', 'g', 'k' ]
    plt.subplot(5, 1, 1)
    make_plots(x, y, label='Входные данные из: ' + filename + '\n' + 'Длина: ' + str(len(y)), color='m')
    for i, keys in enumerate(names):
        plt.subplot(5, 1, i + 2)
        appr_y = pywt.wavedec(y, keys, level=decomp)[ 0 ]
        plt.plot(appr_y, color=colors[ i ], linewidth=3)
        print(f'Дисперсия: {dispersion(appr_y, y)} | {names[ keys ]}')
    plt.gcf().set_size_inches(15, 12)

def continuos_wavelet_three_dimensional(x: list, y: list, level: int, method: str):
    """
         Функция считает и выводи апроксимации для функций на основе X,Y значений и декомпозиции
         :params x: list - X-значения

         :params y: list - Y-значения

         :params level: int - уровень растяжения (2**level)

         :params method: str - тип вейвлета, который распознается библиотекой pywt

         :params filename: str - имя файла
    """
    # вейвлет
    widths = np.arange(1, 2 ** (level) - 1)
    cwtmatr, freqs = pywt.cwt(y, widths, method)
    # cwtmattr - аппроксимация
    # freqs - декомпозиция

    fig, axs = plt.subplots(2)  # задание формы для построения двух сабплотов

    axs[ 0 ].plot(x, y)
    axs[ 0 ].set_title('Данные из CSV-файла')
    axs[ 0 ].grid()

    # построение вейвлет-графика
    axs[ 1 ].imshow(cwtmatr, extent=[ -1, 1, 1, 2 ** (level) - 1 ], cmap='PuRd', aspect='auto',
                    vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())
    axs[ 1 ].set_title(f'3D CWT с уровнем растяжения 2^{level}')
    fig.tight_layout()
    fig.show()