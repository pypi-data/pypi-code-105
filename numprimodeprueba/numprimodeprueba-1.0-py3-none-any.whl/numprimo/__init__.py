# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 11:03:50 2021

@author: ALEXANDRA
"""

def num_primo(n):
    if n ==1 or n==0:
        return False
    elif n== 2:
        return True
    elif n > 2:
        for c in range (2, n):
            if n % c == 0:
                return False
            elif n % c !=0 and c == n-1:
                return True
            
print (num_primo(19))
            
            


            