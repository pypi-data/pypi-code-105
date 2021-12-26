def reduce(iterable, acc, fun):
    for x in iterable:
        acc = fun(x, acc)
    return acc
