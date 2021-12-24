from cacheout import Cache

# global cache object:
_CACHE = Cache()


def get(key, default=None):
    global _CACHE
    return _CACHE.get(key, default)


def set(key, value, ttl=None):
    global _CACHE
    _CACHE.set(key, value, ttl)


def delete(key):
    global _CACHE
    _CACHE.delete(key)


