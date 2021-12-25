from functools import wraps
from inspect import iscoroutinefunction
from types import MethodType

from fastack_cache.backends.base import BaseCacheBackend


def auto_connect(method: MethodType):
    if iscoroutinefunction(method):

        @wraps(method)
        async def wrapper(*args, **kwargs):
            self: BaseCacheBackend = args[0]
            if not self.client:
                await self.connect()
            return await method(*args, **kwargs)

    else:

        @wraps(method)
        def wrapper(*args, **kwargs):
            self: BaseCacheBackend = args[0]
            if not self.client:
                self.connect()
            return method(*args, **kwargs)

    return wrapper
