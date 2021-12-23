import csv
from scipy.fft import rfft, rfftfreq, irfft
from pywt import wavedec
import pywt
import numpy as np

def read_csv(filename):
    
    """
    Функция для получения данных x, y координат из файла .csv

    Parameters
    ----------
    filename : str
        Абсолютный или локальный путь до файла .csv

    Returns
    -------
    my_list : [float, float, ...]
        Список координат x
    my_list2 : [float, float, ...]
        Список координат y

    """
    
    filename = input()
    with open(filename, 'r') as file:
        data = csv.reader(file, delimiter=',')
        data = list(data)
        my_list = []
        my_list2 = []
        for i in range(len(data)):
            my_list.append(eval(data[i][0]))
            my_list2.append(eval(data[i][1]))
    return my_list, my_list2



def custom_fft(x_list, y_list, do_ifft=False):
    """
    Функция БПФ (Быстрое Преобразование Фурье)

    Parameters
    ----------
    x_list : [float, float, ...]
        Координаты х исходного сигнала
    y_list : [float, float, ...]
        Координаты y исходного сигнала
    do_ifft : bool, optional
        True - функция вернёт так-же востановленный сигнал. 
        По умолчанию - False.

    Returns
    -------
    X : [float, float, ...]
        Список частот
    Y : [float, float, ...]
        Список коеффициентов частот
    Y1 : [float, float, ...], optional
        Список значений востановленного сигнала, 
        возвращается только при do_ifft == True
    """
    
    period = (len(x_list))/(x_list[-1] - x_list[0])
    X = rfftfreq(len(x_list), 1 / period)
    fft_y = rfft(y_list)
    Y = [abs(el) for el in fft_y]
    if do_ifft:
        ifft_y = irfft(fft_y)
        Y1 = [el.real for el in ifft_y]
        return X, Y, Y1
    return X, Y



def no_sin_coef(X, Y):
    """
    Функция вычисления коэффициента несинусоидальности

    Parameters
    ----------
    X : [float, float, ...]
        Список частот
    Y : [float, float, ...]
        Список коеффициентов частот

    Returns
    -------
    coef : float
        Коэффициент несинусоидальности сигнала

    """
    
    step = X[1] - X[0]
    step = X[1] - X[0]
    s0 = ((Y[Y.index(max(Y)) + 1] + Y[Y.index(max(Y)) - 1])/2 + Y[Y.index(max(Y))])*step
    si = 0
    for i in range(1, len(Y)):
        si += (Y[i-1] + Y[i])* step/2
    coef = (si-s0)/s0
    return coef



def dobeshi(y, level):
    """
    Функция вычисления декомпозиции на основе вейвлет преобразования Добеши

    Parameters
    ----------
    y : [float, float, ...]
        Список коеффициентов частот
    level : int
        Уровень декомпозиции

    Returns
    -------
    coef : [float, float, ...]
        Список значений докемпозиции

    """
    
    coeffs = wavedec(y, 'db5', level=level)[1]
    return coeffs



def haar(y, level):
    """
    Функция вычисления декомпозиции на основе вейвлет преобразования Хааре

    Parameters
    ----------
    y : [float, float, ...]
        Список коеффициентов частот
    level : int
        Уровень декомпозиции

    Returns
    -------
    coef : [float, float, ...]
        Список значений докемпозиции

    """
    
    coeffs = wavedec(y, 'haar', level=level)[1]
    return coeffs



def wavelets_4lvl_gm(signal, level=1):
    """
    

    Parameters
    ----------
    signal : [float, float, ...]
        Список коеффициентов частот
    level : int, optional
        Уровень декомпозиции. По умолчанию 1.
        Доступны лишь значения 1, 2, 3, 4

    Raises
    ------
    ValueError
        Возникает при передаче level не входящего в интервал [1; 4].

    Returns
    -------
    coef : [float, float, ...]
        Список значений докемпозиции

    """
    
    if level < 1 or level > 4:
        raise ValueError('Доступные уровни декомпозиции: 1, 2, 3, 4')
    wavelet = pywt.ContinuousWavelet('mexh')
    coef1, freqs1 = pywt.cwt(signal, np.arange(1, 30), wavelet)
    coef2, freqs2 = pywt.cwt(coef1[0], np.arange(1, 30), wavelet)
    coef3, freqs3 = pywt.cwt(coef2[0], np.arange(1, 30), wavelet)
    coef4, freqs4 = pywt.cwt(coef3[0], np.arange(1, 30), wavelet)
    coefs = [coef1, coef2, coef3, coef4]
    coef = coefs[level - 1]
    return coef