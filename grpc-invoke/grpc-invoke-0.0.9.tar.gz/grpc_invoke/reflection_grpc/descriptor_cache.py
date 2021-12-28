from datetime import datetime, timedelta

from google.protobuf.descriptor import Descriptor


class DescriptorData(object):
    def __init__(self, desc: Descriptor, expired_time: int = 3600):
        """
        default expired time is one hour
        :param expired_time:
        """
        now = datetime.now()
        self.exp_time = now + timedelta(seconds=expired_time)
        self.desc = desc

    @property
    def expire_time(self):
        return self.exp_time

    @property
    def descriptor(self):
        return self.desc


class DescriptorCache(object):
    """
    cache for file descriptor
    """
    _cache = None

    def __init__(self):
        self._cache = dict()

    def get_descriptor(self, name: str):
        """
        get descriptor from cache
        :param name:
        :return:
        """
        data = self._cache.get(name)
        if data is None:
            return None
        if data.expire_time > datetime.now():
            return data.descriptor
        del data[name]
        return None

    def set_descriptor(self, name: str, descriptor, expired_time=3600):
        """
        set descriptor to cache
        :param name: key name
        :param descriptor:
        :param expired_time:
        :return:
        """
        data = DescriptorData(descriptor, expired_time)
        self._cache[name] = data
        return data.descriptor


file_cache = DescriptorCache()
