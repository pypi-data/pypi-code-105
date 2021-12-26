from eyja.db.rethinkdb import RethinkDBClient
from eyja.db.redis import RedisClient
from eyja.errors import ParseModelNamespaceError

from .config_hub import ConfigHub


class DataHub:
    _connections = {
        'rethinkdb': {},
        'redis': {},
    }

    @classmethod
    async def init(cls, config = None):
        if not config:
            ConfigHub.load_from_file()
        else:
            ConfigHub.load(config)

        await cls.init_rethinkdb()
        await cls.init_redis()

    @classmethod
    async def init_rethinkdb(cls):
        for _config in ConfigHub.rethinkdb():
            cls._connections['rethinkdb'][_config.name] = RethinkDBClient(_config)
            await cls._connections['rethinkdb'][_config.name].init()

    @classmethod
    async def init_redis(cls):
        for _config in ConfigHub.redis():
            cls._connections['redis'][_config.name] = RedisClient(_config)
            await cls._connections['redis'][_config.name].init()

    @classmethod
    def get_connection(cls, obj):
        namespaces = obj.Internal.namespace.split(':')
        if len(namespaces) != 4:
            raise ParseModelNamespaceError(
                'A namespace must have four parts - storage type, storage connection, objectspace, and object type - separated by ":"'
            )

        storage_type = namespaces[0]
        storage_connection = namespaces[1]
        object_space = namespaces[2]
        object_type = namespaces[3]

        if len(storage_connection) < 1:
            storage_connection = 'default'

        if storage_type not in cls._connections:
            raise ParseModelNamespaceError(
                'Unknown storage type'
            )

        if storage_connection not in cls._connections[storage_type]:
            raise ParseModelNamespaceError(
                f'Unknown storage connection - [{storage_connection}]'
            )

        return (
            cls._connections[storage_type][storage_connection],
            object_space, object_type,
        )

    @classmethod
    async def save(cls, obj):
        connection, object_space, object_type = cls.get_connection(obj)
        await connection.save(obj, object_space, object_type)

    @classmethod
    async def delete(cls, obj):
        connection, object_space, object_type = cls.get_connection(obj)
        await connection.delete(obj, object_space, object_type)

    @classmethod
    async def get(cls, obj_cls, object_id):
        connection, object_space, object_type = cls.get_connection(obj_cls)
        return await connection.get(obj_cls, object_space, object_type, object_id)

    @classmethod
    async def find(cls, obj_cls, filter):
        connection, object_space, object_type = cls.get_connection(obj_cls)
        return await connection.find(obj_cls, object_space, object_type, filter)
