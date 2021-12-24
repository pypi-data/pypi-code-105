def plus_1(a):
    return a + 1


def plus_n(a, n):
    if n == 1:
        return plus_1(a)
    elif n < 0:
        return -plus_n(-a, -n)
    else:
        return plus_1(plus_n(a, n - 1))
