from numpy import arange
import numpy as np
import random


def probability(N):
    dots = []
    for i in arange(0.0, 1.0, 1 / 15):
        dots.append(i)
    cnt = 0
    for i in range(N + 1):
        for d in range(3):
            rdot = random.choice(dots)
            helpi = dots.index(rdot)
            x = np.random.uniform(0, 1)
            if helpi == 14:
                if rdot <= x <= 1:
                    cnt += 1
                    break
            if rdot <= x <= dots[helpi + 1]:
                cnt += 1
                break

    return "probability = {}".format(cnt / N)