import requests
import os

from abc import ABC, abstractmethod
from enum import Enum

from cloudml import settings

class BaseItemHandler(ABC):

    @abstractmethod
    def get_data(self, relative_path):
        return None


class CacheItemHandler(BaseItemHandler):

    @abstractmethod
    def set_data(self, meta, data):
        pass


class LRUCacheItemHanddler(CacheItemHandler):
    pass


class FileCacheType(Enum):
    localfs = 1
    memfs = 2


class FileCacheItemHandler(CacheItemHandler):
    def __init__(self, root):
        self._root = root

    def get_data(self, relative_path):
        abs_path = '/'.join(self._root, relative_path)
        with open(abs_path, 'b') as f:
            content = f.read()
        return content

    def set_data(self, relative_path, data):
        abs_path = self._root + '/' + relative_path
        path = os.path.dirname(abs_path)
        if os.path.exists(path):
            pass
        else:
            os.makedirs(path)
        with open(abs_path, 'wb') as f:
            content = f.write(data)
        return content


class RawItemhandler(BaseItemHandler):

    def set_cache_handler(self, hdr : FileCacheItemHandler):
        self._cache_handler = hdr
 
    def cache_handler(self) -> FileCacheItemHandler:
        return self._cache_handler
    
    def get_and_cache(self, relative_path):
        data = self.get_raw_data(self.get_prefix(), relative_path)
        if self.cache_handler():
            self.cache_handler().set_data(relative_path, data)
        return data
    
    def get_data(self, relative_path):
        if settings.ENABLE_SET_CACHE_WHEN_GET:
            return self.get_and_cache(relative_path)
        else: 
            return self.get_raw_data(self.get_prefix(), relative_path)

    @abstractmethod
    def get_prefix(self):
        pass

    @abstractmethod
    def get_raw_data(self, prefix, relative_path):
        pass


# basic Item handler
class HttpItemHandler(RawItemhandler):
    def __init__(self, prefix):
        self.prefix = prefix


    def get_raw_data(self, prefix, relative_path):
        url = prefix + '/' + relative_path
        resp = requests.get(url)
        return resp.content

    def get_prefix(self):
        return self.prefix


class FDSItemHandler(RawItemhandler):
    pass


class SFSItemHandler(RawItemhandler):
    pass


class ADRNItemHandler(RawItemhandler):
    pass


class ItemHandlerGenerator(object):

    @classmethod
    def gen_from_item_prefix(cls, prefix) -> RawItemhandler:
        if prefix.startswith("http"):
            return HttpItemHandler(prefix)
        else:
            raise Exception("meta : {}  is not support! ".format(prefix))
    
    @classmethod
    def gen_for_file_cache(cls, dataset_name, dataset_version, cache_type : FileCacheType) -> FileCacheItemHandler:
        if dataset_name:
            pass
        else:
            dataset_name = "default_name"
        if dataset_version:
            pass
        else:
            dataset_version = "default_version"
        if cache_type == FileCacheType.localfs:
            return FileCacheItemHandler('/'.join([settings.LOCAL_CACHE_ROOT_PATH, dataset_name, dataset_version]))
        elif cache_type == FileCacheType.memfs:
            return FileCacheItemHandler('/'.join([settings.MEM_CACHE_ROOT_PATH, dataset_name, dataset_version]))
        else:
            raise Exception("cache_type : {}  is not support! ".format(cache_type))