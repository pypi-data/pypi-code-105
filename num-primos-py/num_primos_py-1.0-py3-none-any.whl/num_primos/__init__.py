#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Kevin Almendarez
"""
def get_num_primos(num):
	primes = []
	
	for n in range(1, num):
		if n == 1:
			primes.append(n)
		else:
			count_not_prime = 0
			for j in range(2, n + 1):
				if n % j == 0:
					count_not_prime += 1

			if count_not_prime == 1:
				primes.append(n)

	return primes

number = int(input("Enter number: "))
print("Prime numbers: " + str(get_num_primos(number)))
