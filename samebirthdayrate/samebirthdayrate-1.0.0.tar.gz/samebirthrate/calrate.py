#!/usr/bin/python
#-*-coding:utf-8-*-

import sys

"""
author: gadfy
create time: 2021.12.31
"""

def _afunc(m, n):
    """
    A(m,n) e.g. A(365,1)
    """
    res = 1
    for i in range(n):
        res *= (m - i)
    return res 


def _nfunc(m, n):
    """
    m exp n
    """
    res = 1
    for i in range(n):
        res *= m
    return res

def same_birthday_rate(n=50):
    percent = round(100 - _afunc(365, n)*100.0 / _nfunc(365, n), 2)
    return "{}%".format(percent)

if __name__ == "__main__":
    try:
        num = int(sys.argv[1])
    except Exception as e:
        print "\033[31mparms error, usage: python calrate.py count of days\033[0m" 
        exit(0)
    print same_birthday_rate(23)
