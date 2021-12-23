# pylint: skip-file
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
