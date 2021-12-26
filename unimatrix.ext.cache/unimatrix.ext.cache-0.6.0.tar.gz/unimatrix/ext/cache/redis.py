"""Declares :class:`RedisCache`."""
import typing

import aioredis

from .base import BaseCache


class RedisCache(BaseCache):

    class query_class:
        def __init__(self, iterator):
            self.iterator = iterator
        async def __aiter__(self):
            return 1
        async def __anext__(self):
            raise NotImplementedError

    @property
    def dsn(self):
        """Return the Data Source Name (DNS) for the Redis
        connection.
        """
        dsn = f'redis://{self.opts.host}:{self.opts.port}'
        if self.opts.get('database'):
            dsn = f'{dsn}/{self.opts.database}?'
        return dsn

    @BaseCache.needs_connection
    async def delete(self, name, version=None):
        """Delete a key from the cache."""
        return await self._impl.delete(self.abskey(name, version))

    async def filter(self,
        pattern: str,
        version: int = 1,
        count: int = 100
    ) -> typing.AsyncIterator:
        """Filter keys in the cache by the given match pattern."""
        pattern = f'{self.prefix}:{pattern}:{version}'
        async for k in self._impl.scan_iter(match=pattern, count=count):
            prefix, *parts, version = str.split(bytes.decode(k), ':')
            yield ':'.join(parts)

    @BaseCache.needs_connection
    async def get(self, name, version=None, decoder=None):
        """Get a key from the cache."""
        return await self._impl.get(self.abskey(name, version))

    async def purge(self) -> None:
        """Purges all keys from the cache, for all versions."""
        pass

    @BaseCache.needs_connection
    async def set(self, name, value, version=None, expires=None):
        """Set a key in the cache."""
        await self._impl.set(
            self.abskey(name, version),
            value,
            px=expires
        )

    @BaseCache.needs_connection
    async def setcounter(self, name: str, value: int = 1, expires=None):
        """Create a counter."""
        count = await self._impl.incrby(self.abskey(name, 1), value)
        if value == count and expires is not None:
            await self._impl.pexpire(name=self.abskey(name, 1), time=expires)
        return count

    async def connect(self):
        """Connect to the Redis service."""
        assert self._impl is None # nosec
        self._pool = aioredis.ConnectionPool.from_url(
            self.dsn, decode_responses=False
        )
        self._impl = aioredis.Redis(connection_pool=self._pool)

    async def join(self):
        """Waits until the connection is closed."""
        await self._pool.disconnect()

    def close(self):
        """Closes the connection with the cache server."""
        pass
