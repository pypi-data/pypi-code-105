from slugify import slugify

from .data_model import DataModel
from .base_redis_internal import BaseRedisInternal


class RedisDataModel(DataModel):
    class Internal(BaseRedisInternal):
        pass

    @property
    def key(self):
        result = []

        key_template_nodes = self.Internal.key_template.split('.')
        for node in key_template_nodes:
            if hasattr(self, node):
                result.append(slugify(getattr(self, node)))
            else:
                result.append(node)

        return '.'.join(result)

    @classmethod
    def filtered_key(cls, filter = {}):
        result = []

        key_template_nodes = cls.Internal.key_template.split('.')
        for node in key_template_nodes:
            if node in filter:
                result.append(slugify(filter[node]))
            else:
                result.append('*')

        return '.'.join(result)
