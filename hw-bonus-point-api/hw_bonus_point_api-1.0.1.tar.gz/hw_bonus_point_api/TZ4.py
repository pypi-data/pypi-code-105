#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import csv
import copy
import random
y=np.array([])
with open("cure.csv",encoding='utf-8-sig') as f:
    reader = csv.reader(f,delimiter=";")
    for row in reader:
        y=np.append(y,float(row[0]))
x = np.array(range(1,854))

PointsINMIn = argrelextrema(y, np.less_equal,order=20)[0]
PointsINMax = argrelextrema(y, np.greater_equal,order=20)[0]
Yy=copy.deepcopy(y)
Pairs=[]
plt.figure(figsize=(18,10))
plt.plot(x,y,c="red")
plt.title("Локальные экстремчики")
plt.scatter(PointsINMIn,y[PointsINMIn], c = "black")
plt.scatter(PointsINMax,y[PointsINMax],c="blue")
plt.show()
if (PointsINMIn[0]<PointsINMax[0]):
    a=1
else:
    a=0

if (PointsINMIn[-1]>PointsINMax[-1]):
    q=1
else:
    q=0
PointsINMInCheck=list(PointsINMIn)
PointsINMaxCheck=list(PointsINMax)

n=0

def greenPointsForCheck():
    if a==1:
        if PointsINMaxCheck[n+1]<PointsINMInCheck[n+1]:
            PointsINMaxCheck.pop(n+1)
            greenPointsForCheck()
    if a==0:
        if PointsINMaxCheck[n+1]<PointsINMInCheck[n]:
            PointsINMaxCheck.pop(n+1)
            greenPointsForCheck()


def appr_kx(x,y):
    from scipy.linalg import solve
    import matplotlib.pyplot as plt
    kx = solve([[sum([i ** 2 for i in x]), sum(x)], [sum(x), len(x)]],
               [[sum([y[i] * x[i] for i in range(len(x))])], [sum(y)]])
    x1 = []
    y1 = []
    for i in range(int(min(x)), int(max(x)) + 1):
        x1.append(i)
        y1.append(kx[0][0] * i + kx[1][0])
    print(f'y = {round(kx[0][0])}x+{round(kx[1][0])}')
    print()
    for ind, el in enumerate(x):
        print(f'x:{el} y:{y[ind]} fi:{round(kx[0][0] * el + kx[1][0])}')
    print()
    print(f'Дисперсия {sum([(y[ind] - kx[0][0] * el + kx[1][0]) ** 2 for ind, el in enumerate(x)])}')
    plt.plot(x1, y1)
    plt.scatter(x, y)
    return x1,y1

def appr_ax(x,y):
    from scipy.linalg import solve
    import matplotlib.pyplot as plt
    kx = solve([[sum([i ** 4 for i in x]), sum([i ** 3 for i in x]), sum([i ** 2 for i in x])],
                [sum([i ** 3 for i in x]), sum([i ** 2 for i in x]), sum([i ** 1 for i in x])],
                [sum([i ** 2 for i in x]), sum([i ** 1 for i in x]), len(x)]],
               [[sum([(x[i] ** 2) * y[i] for i in range(len(x))])],
                [sum([x[i] * y[i] for i in range(len(x))])],
                [sum([y[i] for i in range(len(x))])]])

    x1 = []
    y1 = []
    for i in range(int(min(x)) * 10, (int(max(x)) + 1) * 10):
        x1.append(i / 10)
        y1.append(kx[0][0] * (i / 10) ** 2 + kx[1][0] * i / 10 + kx[2][0])
    print(f'y = {round(kx[0][0])}x**2+{round(kx[1][0])}x + {round(kx[2][0])}')
    print()
    for ind, el in enumerate(x):
        print(f'x:{el} y:{y[ind]} fi:{kx[0][0] * (el) ** 2 + kx[1][0] * el + kx[2][0]}')
    print()
    print(
        f'Дисперсия {sum([(y[ind] - kx[0][0] * (x[ind]) ** 2 + kx[1][0] * x[ind] + kx[2][0]) ** 2 for ind, el in enumerate(x)])}')
    plt.plot(x1, y1)
    plt.scatter(x, y)
    return x1,y1

def RedPointsForCheck():
    if a==1:
        if PointsINMInCheck[n+1]<PointsINMaxCheck[n]:
            PointsINMInCheck.pop(n+1)
            RedPointsForCheck()
    if a==0:
        if PointsINMInCheck[n+1]<PointsINMaxCheck[n+1]:
            PointsINMInCheck.pop(n+1)
            RedPointsForCheck()
while (n<=len(PointsINMaxCheck)-2):
    greenPointsForCheck()
    RedPointsForCheck()
    greenPointsForCheck()
    RedPointsForCheck()
    n=n+1
n=0

#while (n<=len(PointsINMInCheck)-2):
 #   RedPointsForCheck()
#    n=n+1
#n=0



print(PointsINMInCheck)
print(PointsINMaxCheck)
n=0
while n<len(PointsINMInCheck)-2:
    Pairs.append([PointsINMInCheck[n],PointsINMaxCheck[n]])
    Pairs.append([PointsINMaxCheck[n],PointsINMInCheck[n+1]])
    n=n+1
print(Pairs)
MainPoimt=[]
a=0
while a<len(Pairs):
    XXX=round((Pairs[a][0]+Pairs[a][1])/2)
    MainPoimt.append(XXX)
    a=a+1
print(MainPoimt)
plt.figure(figsize=(18, 10))
plt.plot(x,y)
plt.title("Выборки для апроксимации")
plt.scatter(PointsINMInCheck,y[PointsINMInCheck],c="r")
plt.scatter(PointsINMaxCheck,y[PointsINMaxCheck],c="g")

for a in MainPoimt:
    plt.axvline(a,0,100,c="r")
print(y[30]-30)
plt.show()
ThangS=[]
ThangS2=[]
Expa1=[]
Expa2=[]
Expa3=[]
Expa4=[]
Dispp=0
for n in range(len(MainPoimt) - 1):

    Ymeans = []
    Xmeans = []
    cout = random.randint(0, 1)
    III = MainPoimt[n]
    while (III <= MainPoimt[n + 1]):
        Ymeans.append(y[III])
        Xmeans.append(x[III])
        III += 1
    x0 = MainPoimt[n]
    x1 = MainPoimt[n + 1]
    y0diff = []
    y1diff = []


    will2 = appr_kx(Xmeans,Ymeans)
    will1 = appr_ax(Xmeans,Ymeans)
    Ya5 = []
    Ya6 = []
    for ii in range(len(Ymeans)):
        y0diff.append((Ymeans[ii] - will2[1][ii]) ** 2)
        y1diff.append((Ymeans[ii] - will1[1][ii]) ** 2)
    Ya5 = appr_ax(Xmeans,Ymeans)
    Ya6 = appr_kx(Xmeans,Ymeans)
    if y0diff[-1] <= y1diff[-1]:
        will = appr_ax(Xmeans,Ymeans)
        Dispp = y0diff[-1] + Dispp
    if y0diff[-1] > y1diff[-1]:
        will = appr_kx(Xmeans,Ymeans)
        Dispp = y1diff[-1] + Dispp
    ThangS += will[0]
    ThangS2 += will[1]
    Expa1 += Ya5[0]
    Expa2 += Ya5[1]
    Expa3 += Ya6[0]
    Expa4 += Ya6[1]
Hah1=round(sum(y0diff),3)
Hah2=round(sum(y1diff),3)
Dispp=round(Dispp,3)
plt.subplot(2,3,1)
plt.show()
plt.plot(Expa1,Expa2,c="red")
plt.text(900, 75, Hah2, fontsize=15)
plt.text(800, 75,"Disp=", fontsize=15)
plt.title("Квадратичная кусочная аппроксимация")
plt.show()
#plt.subplot(2,3,1)
plt.text(1000, 75, Hah1, fontsize=15)
plt.text(800, 75,"Disp=", fontsize=15)
plt.plot(Expa3,Expa4,c="red")
plt.title("Линейная кусочная аппроксимация")
plt.show()
#plt.subplot(2,3,1)
plt.text(1000, 75, Dispp, fontsize=15)
plt.text(800, 75,"Disp=", fontsize=15)
plt.plot(ThangS,ThangS2, c="red")
plt.title("Кусочная аппроксимация обоими методами, зависимыми от дисперсии")
plt.show()

