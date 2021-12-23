import time
from functools import wraps

def timethis(func):
    @wraps(func)
    def wrapper(*args, **kw):
        start = time.time()
        result = func(*args, *kw)
        end = time.time()
        print(func.__name__, end-start)
        return result
    return wrapper


@timethis
def add(*args):
    return sum(args)

add.__wrapped__, add.__wrapped__(3,4,5)