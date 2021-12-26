def generator_map(iterable, fun):
    return (fun(x) for x in iterable)


def generator_filter(iterable, fun):
    return (x for x in iterable if fun(x))
