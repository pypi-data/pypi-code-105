from functools import wraps
from types import MethodType

from fastack_cache.backends.base import BaseCache


def auto_connect(method: MethodType):
    @wraps(method)
    def wrapper(*args, **kwargs):
        self: BaseCache = args[0]
        if not self.client:
            self.connect()
        return method(*args, **kwargs)

    return wrapper
