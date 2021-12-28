#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import time

n = int(input("Enter a Number: "))
l = int(input("How many numbers should be displayed? "))
start = time.perf_counter()


def primesfrom2to(q):
    # https://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python/3035188#3035188
    sieve = np.ones(n // 3 + (n % 6 == 2), dtype=bool)
    sieve[0] = False
    for i in range(int(n**0.5) // 3 + 1):
        if sieve[i]:
            k = 3 * i + 1 | 1
            sieve[((k * k) // 3)::2 * k] = False
            sieve[(k * k + 4 * k - 2 * k * (i & 1)) // 3::2 * k] = False
    return np.r_[2, 3, ((3 * np.nonzero(sieve)[0] + 1) | 1)]


p = primes1b = primesfrom2to(n)
s = strong1b = [t for s, t, u in zip(p, p[1:], p[2:]) if t > (s + u) / 2]
w = weak1b = [t for s, t, u in zip(p, p[1:], p[2:]) if t < (s + u) / 2]
b = balanced1b = [t for s, t, u in zip(p, p[1:], p[2:]) if t == (s + u) / 2]

print(f"The first {l} strong primes:", s[:l])
print(f'The count of the strong primes below {n}:', sum(1 for p in s if p < n))
print(f'The count of the strong primes below {n}:', len(s))
print(f'\nThe first {l} weak primes:', w[:l])
print(f'The count of the weak primes below {n}:', sum(1 for p in w if p < n))
print(f'The count of the weak primes below {n}:', len(w))
print(f'\nThe first {l} balanced primes:', b[:l])
print(f'The count of balanced primes below {n}:', len(b))
print(f'TOTAL primes below {n}:', len(p))

finish = time.perf_counter()
print(f"Done in {finish - start:0.4f} seconds")
