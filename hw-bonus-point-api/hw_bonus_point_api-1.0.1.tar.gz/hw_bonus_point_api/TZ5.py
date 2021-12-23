#!/usr/bin/env python
# coding: utf-8

# #### Библиотеки

# In[13]:


#  Математика  #
import numpy as np
import pywt
from sympy import *
from numpy import transpose
from numpy import linalg as LA
from fractions import Fraction
from scipy.fft import fft, ifft
#  Время  #
import time
# График #
import matplotlib.pyplot as plt
from matplotlib import rcParams
plt.rcParams['font.size'] = 36
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'cm'
#  Другое  #
import webbrowser
import random
import copy
import csv


# #### Функции

# In[2]:


def csv_reader(string,sep):
    with open(string,newline='') as csvfile:
        reader = csv.reader(csvfile,delimiter=sep)
        lst=[]
        for row in reader:
            lst.append(list(row))
    return lst


# #### Основной код

# In[59]:


print('Доступные для тестирования файлы: \n 1) Test_sin.csv \n 2) sin_peak.csv \n 3) Line.csv \n 4) 2_sin_5_4.5.csv \n 5) RC_F12_11_2017_T12_11_2021.csv')
string = str(input('Введите название файла, который вы хотите протестировать: '))
sep = str(input('Укажитель разделитель (, или ;): '))
m=csv_reader(string,sep)
for i in range(len(m)):
    m[i][0]=float(m[i][0])
    m[i][1]=float(m[i][1])
    print(f'Значение {i+1}: [{m[i][0]},{m[i][1]}]')


# In[60]:


x = [m[i][0] for i in range(len(m))]
y = [m[i][1] for i in range(len(m))]
fi = list(fft(np.array(y)))
fi2 = list(ifft(fi))

coef_sin = abs((max(fi)/(sum(fi)-max(fi))).real)
print(f'Коэффициент несинусоидальности = {coef_sin}.')

disp = sum([(fi[i]-fi2[i])**2 for i in range(len(fi))]).real
print(f'Дисперсия = {disp}.')

rcParams['figure.figsize'] = (40, 30)
rcParams['figure.dpi'] = 400

plt.subplot(3, 1, 1)

plt.plot(x,y,color='black',lw=2)
plt.grid(b=True, color='DarkTurquoise', alpha=0.75, linestyle=':', linewidth=1)
plt.title(f'Изначальный сигнал. Файл {string}.',fontsize=28, loc = 'right')
plt.tick_params(labelsize = 40)
plt.xlabel('X',fontsize=25)
plt.ylabel('Y',fontsize=25)

plt.subplot(3, 1, 2)

plt.plot(x,fi,color='black',lw=2)
plt.grid(b=True, color='DarkTurquoise', alpha=0.75, linestyle=':', linewidth=1)
plt.title(f'Спектрограмма. Файл {string}.',fontsize=28, loc = 'right')
plt.tick_params(labelsize = 40)
plt.xlabel('X',fontsize=25)
plt.ylabel('Y',fontsize=25)
plt.show()

plt.subplot(3, 1, 3)

plt.plot(x,fi2,color='black',lw=2)
plt.grid(b=True, color='DarkTurquoise', alpha=0.75, linestyle=':', linewidth=1)
plt.title(f'Восстановленная функция. Файл {string}.',fontsize=28, loc = 'right')
plt.tick_params(labelsize = 40)
plt.xlabel('X',fontsize=25)
plt.ylabel('Y',fontsize=25)
plt.show()


# In[42]:


def wav_sinus_coeff(coeffs):
    a4, d4, d3, d2, d1 = coeffs
    result = sqrt(np.std(d4) + np.std(d3) + np.std(d2) + np.std(d1)) / np.std(a4)
    return result


# ##### Daubechies (db)

# In[61]:


x = [i[0] for i in m]
y = [i[1] for i in m]
coeffs = pywt.wavedec(y, 'db5', level=4)

rcParams['figure.figsize'] = (40, 30)
rcParams['figure.dpi'] = 400

# Уровень 1

plt.subplot(4, 1, 1)

plt.plot(coeffs[-4],color='black',lw=2)
plt.grid(b=True, color='DarkTurquoise', alpha=0.75, linestyle=':', linewidth=1)
plt.title(f'Daubechies Уровень 1. Файл {string}.',fontsize=28, loc = 'right')
plt.tick_params(labelsize = 40)
plt.xlabel('X',fontsize=25)
plt.ylabel('Y',fontsize=25)

# Уровень 2

plt.subplot(4, 1, 2)

plt.plot(coeffs[-3],color='black',lw=2)
plt.grid(b=True, color='DarkTurquoise', alpha=0.75, linestyle=':', linewidth=1)
plt.title(f'Daubechies Уровень 2. Файл {string}.',fontsize=28, loc = 'right')
plt.tick_params(labelsize = 40)
plt.xlabel('X',fontsize=25)
plt.ylabel('Y',fontsize=25)
plt.show()

# Уровень 3

plt.subplot(4, 1, 3)

plt.plot(coeffs[-2],color='black',lw=2)
plt.grid(b=True, color='DarkTurquoise', alpha=0.75, linestyle=':', linewidth=1)
plt.title(f'Daubechies Уровень 3. Файл {string}.',fontsize=28, loc = 'right')
plt.tick_params(labelsize = 40)
plt.xlabel('X',fontsize=25)
plt.ylabel('Y',fontsize=25)
plt.show()

# Уровень 4

plt.subplot(4, 1, 4)

plt.plot(coeffs[-1],color='black',lw=2)
plt.grid(b=True, color='DarkTurquoise', alpha=0.75, linestyle=':', linewidth=1)
plt.title(f'Daubechies Уровень 4. Файл {string}.',fontsize=28, loc = 'right')
plt.tick_params(labelsize = 40)
plt.xlabel('X',fontsize=25)
plt.ylabel('Y',fontsize=25)
plt.show()

print(f'Коэффициент несинусоидальности: {wav_sinus_coeff(coeffs)}.')


# ##### Haar (haar)

# In[62]:


x = [i[0] for i in m]
y = [i[1] for i in m]
coeffs = pywt.wavedec(y, 'haar', level=4)

rcParams['figure.figsize'] = (40, 30)
rcParams['figure.dpi'] = 400

plt.subplot(4, 1, 1)

plt.plot(coeffs[-4],color='black',lw=2)
plt.grid(b=True, color='DarkTurquoise', alpha=0.75, linestyle=':', linewidth=1)
plt.title(f'Haar Уровень 1. Файл {string}.',fontsize=28, loc = 'right')
plt.tick_params(labelsize = 40)
plt.xlabel('X',fontsize=25)
plt.ylabel('Y',fontsize=25)



plt.subplot(4, 1, 2)

plt.plot(coeffs[-3],color='black',lw=2)
plt.grid(b=True, color='DarkTurquoise', alpha=0.75, linestyle=':', linewidth=1)
plt.title(f'Haar Уровень 2. Файл {string}.',fontsize=28, loc = 'right')
plt.tick_params(labelsize = 40)
plt.xlabel('X',fontsize=25)
plt.ylabel('Y',fontsize=25)
plt.show()



plt.subplot(4, 1, 3)

plt.plot(coeffs[-2],color='black',lw=2)
plt.grid(b=True, color='DarkTurquoise', alpha=0.75, linestyle=':', linewidth=1)
plt.title(f'Haar Уровень 3. Файл {string}.',fontsize=28, loc = 'right')
plt.tick_params(labelsize = 40)
plt.xlabel('X',fontsize=25)
plt.ylabel('Y',fontsize=25)
plt.show()



plt.subplot(4, 1, 4)

plt.plot(coeffs[-1],color='black',lw=2)
plt.grid(b=True, color='DarkTurquoise', alpha=0.75, linestyle=':', linewidth=1)
plt.title(f'Haar Уровень 4. Файл {string}.',fontsize=28, loc = 'right')
plt.tick_params(labelsize = 40)
plt.xlabel('X',fontsize=25)
plt.ylabel('Y',fontsize=25)
plt.show()

print(f'Коэффициент несинусоидальности: {wav_sinus_coeff(coeffs)}.')


# ##### Mexican hat (mexh)

# In[63]:


x = [i[0] for i in m]
y = [i[1] for i in m]
wavelet = pywt.ContinuousWavelet('mexh')
coef, freqs = pywt.cwt(y,np.arange(1,30),wavelet)
endcoef = []
endcoef.append(coef[0])

plt.subplot(4, 1, 1)

plt.plot(coef[0],color='black',lw=2)
plt.grid(b=True, color='DarkTurquoise', alpha=0.75, linestyle=':', linewidth=1)
plt.title(f'Mexican hat Уровень 1. Файл {string}.',fontsize=28, loc = 'right')
plt.tick_params(labelsize = 40)
plt.xlabel('X',fontsize=25)
plt.ylabel('Y',fontsize=25)
coef, freqs = pywt.cwt(coef[0],np.arange(1,30),wavelet)

plt.subplot(4, 1, 2)

plt.plot(coef[0],color='black',lw=2)
plt.grid(b=True, color='DarkTurquoise', alpha=0.75, linestyle=':', linewidth=1)
plt.title(f'Mexican hat Уровень 2. Файл {string}.',fontsize=28, loc = 'right')
plt.tick_params(labelsize = 40)
plt.xlabel('X',fontsize=25)
plt.ylabel('Y',fontsize=25)
coef, freqs = pywt.cwt(coef[0],np.arange(1,30),wavelet)
endcoef.append(coef[0])

plt.subplot(4, 1, 3)

plt.plot(coef[0],color='black',lw=2)
plt.grid(b=True, color='DarkTurquoise', alpha=0.75, linestyle=':', linewidth=1)
plt.title(f'Mexican hat Уровень 3. Файл {string}.',fontsize=28, loc = 'right')
plt.tick_params(labelsize = 40)
plt.xlabel('X',fontsize=25)
plt.ylabel('Y',fontsize=25)
coef, freqs = pywt.cwt(coef[0],np.arange(1,30),wavelet)
endcoef.append(coef[0])

plt.subplot(4, 1, 4)

plt.plot(coef[0],color='black',lw=2)
plt.grid(b=True, color='DarkTurquoise', alpha=0.75, linestyle=':', linewidth=1)
plt.title(f'Mexican hat Уровень 4. Файл {string}.',fontsize=28, loc = 'right')
plt.tick_params(labelsize = 40)
plt.xlabel('X',fontsize=25)
plt.ylabel('Y',fontsize=25)
coef, freqs = pywt.cwt(coef[0],np.arange(1,30),wavelet)
endcoef.append(coef[0])

endcoef.append(sqrt(np.var(coef[-1])))
endcoef.reverse()
coefsin = sqrt(np.std(endcoef[1]) + np.std(endcoef[2]) + np.std(endcoef[3]) + np.std(endcoef[4])) / endcoef[0]
print(f'Коэффициент несинусоидальности: {coefsin}.')


# ##### Gaussian wavelets (gaus)

# In[64]:


x = [i[0] for i in m]
y = [i[1] for i in m]
wavelet = pywt.ContinuousWavelet('gaus5')
coef, freqs = pywt.cwt(y,np.arange(1,30),wavelet)
endcoef = []
endcoef.append(coef[0])

plt.subplot(4, 1, 1)

plt.plot(coef[0],color='black',lw=2)
plt.grid(b=True, color='DarkTurquoise', alpha=0.75, linestyle=':', linewidth=1)
plt.title(f'Gaussian wavelet Уровень 1. Файл {string}.',fontsize=28, loc = 'right')
plt.tick_params(labelsize = 40)
plt.xlabel('X',fontsize=25)
plt.ylabel('Y',fontsize=25)
coef, freqs = pywt.cwt(coef[0],np.arange(1,30),wavelet)

plt.subplot(4, 1, 2)

plt.plot(coef[0],color='black',lw=2)
plt.grid(b=True, color='DarkTurquoise', alpha=0.75, linestyle=':', linewidth=1)
plt.title(f'Gaussian wavelet Уровень 2. Файл {string}.',fontsize=28, loc = 'right')
plt.tick_params(labelsize = 40)
plt.xlabel('X',fontsize=25)
plt.ylabel('Y',fontsize=25)
coef, freqs = pywt.cwt(coef[0],np.arange(1,30),wavelet)
endcoef.append(coef[0])

plt.subplot(4, 1, 3)

plt.plot(coef[0],color='black',lw=2)
plt.grid(b=True, color='DarkTurquoise', alpha=0.75, linestyle=':', linewidth=1)
plt.title(f'Gaussian wavelet Уровень 3. Файл {string}.',fontsize=28, loc = 'right')
plt.tick_params(labelsize = 40)
plt.xlabel('X',fontsize=25)
plt.ylabel('Y',fontsize=25)
coef, freqs = pywt.cwt(coef[0],np.arange(1,30),wavelet)
endcoef.append(coef[0])

plt.subplot(4, 1, 4)

plt.plot(coef[0],color='black',lw=2)
plt.grid(b=True, color='DarkTurquoise', alpha=0.75, linestyle=':', linewidth=1)
plt.title(f'Gaussian wavelet Уровень 4. Файл {string}.',fontsize=28, loc = 'right')
plt.tick_params(labelsize = 40)
plt.xlabel('X',fontsize=25)
plt.ylabel('Y',fontsize=25)
coef, freqs = pywt.cwt(coef[0],np.arange(1,30),wavelet)
endcoef.append(coef[0])

endcoef.append(sqrt(np.var(coef[-1])))
endcoef.reverse()
coefsin = sqrt(np.std(endcoef[1]) + np.std(endcoef[2]) + np.std(endcoef[3]) + np.std(endcoef[4])) / endcoef[0]
print(f'Коэффициент несинусоидальности: {coefsin}.')

