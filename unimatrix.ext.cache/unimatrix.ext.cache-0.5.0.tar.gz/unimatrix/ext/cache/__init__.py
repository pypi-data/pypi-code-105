# pylint: skip-file
import contextlib
import datetime
import math
import time

from .exceptions import Backoff
from .manager import connections


__all__ = []


async def add(
    key: str,
    value: int = 1,
    using: str = 'default',
    *args, **kwargs
):
    """Create a counter under the given key, starting from ``0`` and
    incremented by `value`. Return the latest value.
    """
    return await connections[using].setcounter(key, value, *args, **kwargs)


@contextlib.asynccontextmanager
async def backoff(key: str, using: str = 'default') -> int:
    """Calculate an exponential backoff using a counter. Return an integer
    representing the remaining milliseconds.
    """
    now = int(time.time())
    expires = await get(f'{key}-expires', using=using)
    if expires is not None:
        expires = int.from_bytes(expires, 'big')
        # Use a leeway of one second.
        raise Backoff(int(math.ceil(expires - now)) + 1)

    try:
        yield
        await delete(key, using=using)
        await delete(f'{key}-expires', using=using)
    except Exception:
        # It is assumed here that any exception indicates that an operation
        # has failed and the backoff should be increased.
        now = int(time.time())
        count = await add(key, using=using)
        ttl = int(count * count)
        await set(
            key=f'{key}-expires',
            value=int.to_bytes(now + ttl, 8, 'big'),
            using=using,
            expires=ttl*1000
        )


async def clear(using: str):
    """Purges all keys from the cache."""
    return await connections[using].clear()


async def delete(key, using='default', *args, **kwargs):
    """Delete the given `key` from the cache, if it exists."""
    kwargs.setdefault('version', 1)
    return await connections[using].delete(key, *args, **kwargs)


async def filter(pattern: str, using: str = 'default'):
    """Filter keys in the cache by the given match pattern."""
    return connections[using].filter(pattern)


async def get(key, using='default', *args, **kwargs):
    """Return given `key` from the cache `using`."""
    kwargs.setdefault('version', 1)
    return await connections[using].get(key, *args, **kwargs)


async def purge(using: str) -> None:
    """Purges all keys from the cache, for all versions."""
    return await connections[using].purge()


async def set(key, value, using='default', *args, **kwargs):
    """Set the given `key` to `value`."""
    kwargs.setdefault('version', 1)
    return await connections[using].set(key, value, *args, **kwargs)
