from functools import wraps


def exitify(func):
    @wraps(func)
    def wrapper(*_, **__):
        exit(0)
    return wrapper
