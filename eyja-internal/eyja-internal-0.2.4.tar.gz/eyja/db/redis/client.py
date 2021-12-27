import aioredis
import uuid
import json

from eyja.db.redis import RedisConfig
from eyja.errors import MissedRepresentationError
from eyja.utils import EyjaJSONEncoder


class RedisClient:
    _connection = {}

    def __init__(self, config: RedisConfig):
        self._config = config

    async def _connect(self):
        for db_name, db_id in self._config.db.items():
            self._connection[db_name] = aioredis.from_url(
                f'redis://{self._config.host}:{self._config.port}/{db_id}'
            )

    def get_redis_url(self, db_name):
        return f'redis://{self._config.host}:{self._config.port}/{self._config.db[db_name]}'

    def get_redis_connection(self, db_name):
        return aioredis.from_url(self.get_redis_url(db_name))

    async def init(self):
        pass

    async def save(self, obj, object_space, object_type):
        if 'key' not in dir(obj):
            raise MissedRepresentationError('Missed "key" representation')

        if not obj.object_id:
            obj.object_id = str(uuid.uuid4())

        hierarchical_key = f'{object_type}.{obj.key}'

        async with self.get_redis_connection(object_space).client() as conn:
            await conn.delete(hierarchical_key)

            set_args = [
                hierarchical_key,
                json.dumps(obj.data, cls=EyjaJSONEncoder),
            ]

            if obj.Internal.expiration > 0:
                set_args.append(obj.Internal.expiration)

            await conn.set(*set_args)

    async def delete(self, obj, object_space, object_type):
        if 'key' not in dir(obj):
            raise MissedRepresentationError('Missed "key" representation')

        hierarchical_key = f'{object_type}.{obj.key}'

        async with self.get_redis_connection(object_space).client() as conn:
            await conn.delete(hierarchical_key)

    async def get(self, obj_cls, object_space, object_type, object_id):
        from eyja.db.models import DataFilter

        filter = DataFilter(fields={'object_id': object_id})
        items = await self.find(obj_cls, object_space, object_type, filter)
        
        if len(items) > 0:
            return items[0]
        
        return None

    async def find(self, obj_cls, object_space, object_type, filter):
        result = []

        if 'filtered_key' not in dir(obj_cls):
            raise MissedRepresentationError('Missed "filtered_key" representation')

        search_key = obj_cls.filtered_key(filter.fields)
        hierarchical_key = f'{object_type}.{search_key}'
        async with self.get_redis_connection(object_space).client() as conn:
            keys = await conn.keys(hierarchical_key)
            for key in keys:
                data = await conn.get(key)
                obj_data = json.loads(data)
                result.append(obj_cls(**obj_data))
        
        return result