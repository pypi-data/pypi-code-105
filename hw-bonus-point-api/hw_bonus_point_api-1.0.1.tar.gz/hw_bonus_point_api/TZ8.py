#!/usr/bin/env python
# coding: utf-8

# In[1]:


import copy

import random
import time
import matplotlib.pyplot as plt

print("введите Вершины")
n = int(input())




Q = 4  # константа 
a = 1  # константа 
b = 4  # константа 
Mnojest = {1}
Inters = []
Inters.append(1)
Countries = {}  # Множество городов
MAtrizaPheromonov = {}  # матрица феромончиков
Xsheeesh = []  # x координаты городов
Ysheeesh = []  # y координаты городов
Xsheeesh.append(1)  # Начинаем с 0, а не с 1
Ysheeesh.append(1)  # Начинаем с 0, а не с 1
for i in range(2, n + 1):
    Mnojest.add(i)






for i in range(1, n + 1):
    Xsheeesh.append(random.randint(200, 1500))
    Ysheeesh.append(random.randint(200, 900))


def GeneratorRex():  # Авто генерация путей
    Wow = []
    Wow1 = []
    for i in range(1, n + 1):
        for x in range(1, n + 1):
            Countries[int(str(i) + str(x))] = int(random.randint(100, 1710))
            if x == i:
                Countries[int(str(i) + str(x))] = "a"
            q = 0
            if q == 1:
                Countries[int(str(i) + str(x))] = "a"
            Wow.append(Countries[int(str(i) + str(x))])
        Wow1.append(Wow)
        Wow = []
    for i in Wow1:
        print(i)
        
def MatrizaPher():
    Wow = []
    Wow1 = []
    for i in range(1, n + 1):
        for x in range(1, n + 1):
            MAtrizaPheromonov[int(str(i) + str(x))] = 3
            if x == i:
                MAtrizaPheromonov[int(str(i) + str(x))] = "b"
            q = random.randint(1, 5)
            if Countries[int(str(i) + str(x))] == "a":
                MAtrizaPheromonov[int(str(i) + str(x))] = "b"
            Wow.append(MAtrizaPheromonov[int(str(i) + str(x))])
        Wow1.append(Wow)
        Wow = []
    for i in Wow1:
        print(i)

def GeneratorRex2():
    Wow = []
    Wow1 = []

    for i in range(1, n + 1):
        for x in range(1, n + 1):
            print(i, x, "введите:")
            Countries[int(str(i) + str(x))] = input()
            if x == i:
                Countries[int(str(i) + str(x))] = "a"
            Wow.append(Countries[int(str(i) + str(x))])
        Wow1.append(Wow)
        Wow = []
    for i in Wow1:
        print(i)


print("Авто или ручками (1 или 2)?")
Turn = int(input())
if Turn == 1:
    GeneratorRex()
if Turn == 2:
    GeneratorRex2()
print()
print("МАТРИЦА ФЕРОМОНчиков")
print()
MatrizaPher()


class DarkArmy():
    Piii = 1
    xlocation = Xsheeesh[Piii]
    ylocation = Ysheeesh[Piii]
    xfutlocation = 0
    yfuturelocation = 0
    Saving = copy.deepcopy(Mnojest)
    FutureCountries = []
    FutureCu = 0
    FutureCountriesP = []
    PastCountries = []
    Q = 200
    a = 1
    b = 1
    Y = 4
    Ready = 0
    countoffailures = 2

    def __init__(self, num):
        self.Piii = num
        self.xlocation = Xsheeesh[num]
        self.ylocation = Ysheeesh[num]

        self.Mnojest = {num}
        self.PastCountries = [num]
        print(self.PastCountries)

    def choosetown(self):
        if self.Ready == 0:
            self.FutureCountries = []
            self.FutureCountriesP = []
            for i in range(1, n + 1):
                if type(Countries[int(str(self.Piii) + str(i))]) is int and i not in self.PastCountries:
                    self.FutureCountries.append(int(i))
            if not self.FutureCountries and self.Saving != self.Mnojest:
                self.FutureCu = self.PastCountries[-(self.countoffailures)]
                self.xfutlocation = Xsheeesh[int(self.FutureCu)]
                self.yfuturelocation = Ysheeesh[int(self.FutureCu)]
                self.PastCountries.append(self.FutureCu)
                self.Mnojest.add(self.FutureCu)
                self.countoffailures += 1
            else:
                for i in self.FutureCountries:
                    self.FutureCountriesP.append(((Q / Countries[int(str(self.Piii) + str(i))]) ** 4) * (
                                (MAtrizaPheromonov[int(str(self.Piii) + str(i))]) ** 2))
                self.FutureCu = random.choices(self.FutureCountries, weights=self.FutureCountriesP, k=1)
                self.xfutlocation = Xsheeesh[int(self.FutureCu[0])]
                self.yfuturelocation = Ysheeesh[int(self.FutureCu[0])]
                self.PastCountries.append(self.FutureCu[0])
                self.countoffailures = 2
                self.Mnojest.add(self.FutureCu[0])
            # print(self.PastCountries)

    def NextStep(self):
        if self.Ready == 0:
            self.xlocation = self.xfutlocation
            self.ylocation = self.yfuturelocation

    def check(self):

        if Mnojest == self.Mnojest:
            self.Ready = 1

        return self.Ready


# for i in range(1,n+1):
# KK=random.Turns([Ant1,Ant2,Ant3],[10,10,10])
# Anty[i]=DarkArmy(ANttype=KK[0],num=i)


Nya1 = []
Nya2 = []
Lelwd3 = 0
Counter = 1
hmph = []
MinID = 0
for i in range(80):

    Anty = []
    for i in range(n + 1):
        Anty.append(1)

    for i in range(1, n + 1):
        Anty[i] = DarkArmy(num=i)
    while True:
        for i in range(1, n + 1):
            Anty[i].choosetown()

            time.sleep(0.0000002)
        for i in range(1, n + 1):
            Anty[i].NextStep()
        AAA = 0
        for i in range(1, n + 1):
            AAA += Anty[i].check()

        if AAA == n:
            break
        AAA = 0
    for i in range(1, n + 1):
        for YYY in range(1, n):

            Qar = copy.copy(Anty[i].PastCountries)

            Qar.insert(0, 1)

            if type(MAtrizaPheromonov[int(str(Qar[YYY]) + str(Qar[YYY + 1]))]) is int or float:
                MAtrizaPheromonov[int(str(Qar[YYY]) + str(Qar[YYY + 1]))] = MAtrizaPheromonov[int(str(Qar[YYY]) + str(
                    Qar[YYY + 1]))] * 0.64 + Q / Countries[int(str(Qar[YYY]) + str(Qar[YYY + 1]))]

    Nya1 = copy.copy(Anty[1].PastCountries)
    hmph.append(Nya1)
    Lelwd3 = 0
    for i in range(len(Nya1) - 1):
        Lelwd3 += Countries[int(str(Nya1[i]) + str(Nya1[i + 1]))]
        print(Countries[int(str(Nya1[i]) + str(Nya1[i + 1]))])
    Nya2.append(Lelwd3)

    Counter += 1
Checking = Nya2[0]
for i in range(len(Nya2)):
    if Checking > Nya2[i]:
        Checking = Nya2[i]
        MinID = i

print("самый короткий de way", hmph[MinID], Checking)
print("константы a=4,b=1. Q=300. Относительно оптимальный выбор для дорог сопоставимых с данными экрана (1920*1080)")
plt.plot(range(Counter - 1), Nya2)

plt.show()


# In[ ]:




