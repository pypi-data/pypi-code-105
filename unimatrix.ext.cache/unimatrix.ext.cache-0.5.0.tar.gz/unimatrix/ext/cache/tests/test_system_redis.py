# pylint: skip-file
import asyncio
import os

import unimatrix.lib.test

from unimatrix.ext import cache


@unimatrix.lib.test.needs('redis')
class RedisTestCase(unimatrix.lib.test.AsyncTestCase):
    __test__ = True

    async def setUp(self):
        self.prefix = bytes.hex(os.urandom(16))
        cache.connections.add('default', {
            'backend': 'redis',
            'host': 'localhost',
            'port': 6379,
            'database': 2,
            'prefix': self.prefix,
        })
        await cache.connections.connect()

    async def tearDown(self):
        await cache.purge('default')
        await cache.connections.destroy()

    async def test_filter(self):
        await cache.set('sub-1-whitelist', 'foo')
        await cache.set('sub-1-ips', 'bar')
        keys = []
        async for k in await cache.filter(f'sub-1*'):
            keys.append(k)
        self.assertEqual(len(keys), 2, keys)

    async def test_filter_versioned(self):
        await cache.set('sub-1-whitelist', 'foo')
        await cache.set('sub-1-ips', 'bar')
        await cache.set('sub-1-foo', 'bar', version=2)
        keys = []
        async for k in await cache.filter(f'sub-1*'):
            keys.append(k)
        self.assertEqual(len(keys), 2, keys)

    async def test_set(self):
        k = 'foo'
        await cache.set(k, 'bar')
        self.assertEqual(await cache.get(k), b'bar')

    async def test_set_versioned(self):
        k = 'foo'
        await cache.set(k, 'bar')
        await cache.set(k, 'baz', version=2)
        await cache.set(k, 'taz', version=3)
        self.assertEqual(await cache.get(k), b'bar')
        self.assertEqual(await cache.get(k, version=2), b'baz')
        self.assertEqual(await cache.get(k, version=3), b'taz')

    async def test_set_counter(self):
        self.assertEqual(await cache.add('counter'), 1)
        self.assertEqual(await cache.add('counter'), 2)
        self.assertEqual(await cache.add('counter'), 3)
        self.assertEqual(await cache.add('counter', 2), 5)

        await cache.delete('counter')
        self.assertEqual(await cache.add('counter'), 1)

    async def test_set_counter_expires(self):
        self.assertEqual(await cache.add('counter', expires=500), 1)
        await asyncio.sleep(1)
        self.assertEqual(await cache.add('counter', expires=500), 1)

    async def test_set_expires(self):
        k = 'foo'
        await cache.set(k, 'bar', expires=1000)
        self.assertEqual(await cache.get(k), b'bar')
        await asyncio.sleep(1)
        self.assertEqual(await cache.get(k), None)

    async def test_del(self):
        k = 'foo'
        await cache.set(k, 'bar')
        await cache.delete(k)
        self.assertEqual(await cache.get(k), None)

    async def test_backoff_is_enforced(self):
        key = 'backoff-' + os.urandom(4).hex()
        try:
            async with cache.backoff(key):
                raise NotImplementedError
        except NotImplementedError:
            pass

        with self.assertRaises(cache.Backoff):
            async with cache.backoff(key):
                pass

        try:
            async with cache.backoff(key):
                self.fail("Backoff must be raised.")
        except cache.Backoff as e:
            backoff = e
        self.assertTrue(backoff is not None)
        self.assertEqual(backoff.seconds, 2)
        await asyncio.sleep(backoff.seconds)
        async with cache.backoff(key):
            pass

    async def test_backoff_is_enforced_consequtive(self):
        key = 'backoff-' + os.urandom(4).hex()
        try:
            async with cache.backoff(key):
                raise NotImplementedError
        except NotImplementedError:
            pass

        try:
            async with cache.backoff(key):
                self.fail("Backoff must be raised.")
        except cache.Backoff as e:
            backoff = e
        self.assertEqual(backoff.seconds, 2)
        await asyncio.sleep(backoff.seconds)
        try:
            async with cache.backoff(key):
                raise NotImplementedError
        except NotImplementedError:
            pass
        try:
            async with cache.backoff(key):
                self.fail("Backoff must be raised.")
        except cache.Backoff as e:
            backoff = e
        self.assertEqual(backoff.seconds, 5)
