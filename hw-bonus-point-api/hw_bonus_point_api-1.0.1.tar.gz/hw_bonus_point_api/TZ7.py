#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import copy
import random
from math import exp
import matplotlib.pyplot as plt
Countries = {}
print("введите Вершины")
n = int(input())

def gs(way):
    sum=0
    for i in range(len(way)-1):
        sum+=Countries[int(str(way[i])+str(way[i+1]))]
    return sum
def Generatorrex():  # Авто генерация путей
    Well = []
    Well1 = []
    for i in range(1, n + 1):
        for x in range(1, n + 1):
            Countries[int(str(i) + str(x))] = int(random.randint(1, 20))
            if x == i:
                Countries[int(str(i) + str(x))] = "a"
            q = 0
            if q == 1:
                Countries[int(str(i) + str(x))] = "a"

            Well.append(Countries[int(str(i) + str(x))])
        Well1.append(Well)
        Well = []
    Well = []
    Well1 = []
    for i in range(1, n + 1):
        for x in range(1, n + 1):
            Countries[int(str(i) + str(x))] = Countries[int(str(x) + str(i))]
            Well.append(Countries[int(str(i) + str(x))])
        Well1.append(Well)
        Well = []



def waydown(way):
    counter=[]
    S=way[1:-1]
    S1=random.sample(S,2)
    for i in range(len(S)):
        if S[i]==S1[0]:
            counter.append(i)
        if S[i]==S1[1]:
            counter.append(i)

    timing = S[counter[0]]
    way[counter[0]+1]=S[counter[1]]
    way[counter[1]+1]=timing
    return way
def rnd():
    way=[]
    for i in range(1,n+1):
        way.append(i)
    random.shuffle(way)
    return way
Generatorrex()
x=rnd()
a=0.91
Tempreture=1000
Ll1=gs(x)
Counterstrike=0
Counterstrike2=[]

while Tempreture>0.01:
    Counterstrike+=1
    way3=waydown(x)
    Ll2=gs(way3)
    Difference=Ll2-Ll1
    Notcons=100*exp(-(Difference)/Tempreture)

    if Difference<0:
        Ll1=Ll2
        Tempreture=Tempreture*0.85
        #Counterstrike2.append(Ll1)
    elif Notcons > random.randint(1,100):
        Ll1 = Ll2
        Tempreture = Tempreture * 0.85
        #Counterstrike2.append(Ll1)
    else:
        Tempreture=Tempreture*0.85
    Counterstrike2.append(Ll1)

plt.plot(range(1,Counterstrike+1),Counterstrike2)
plt.show()

