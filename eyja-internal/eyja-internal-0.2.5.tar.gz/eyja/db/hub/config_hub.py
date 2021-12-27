import yaml
import os
import aiofiles

from typing import List

from eyja.db.rethinkdb import RethinkDBConfig
from eyja.db.redis import RedisConfig

from .config import Config


class ConfigHub:
    _config: Config

    @classmethod
    async def load_from_file(cls, config_file = os.environ.get('CONFIG', './config/local.yml')):
        async with aiofiles.open(config_file, 'r') as fp:
            config_data = await fp.read()

        cls.load(config_data)

    @classmethod
    def load(cls, data: str):
        config_data = yaml.load(data, Loader=yaml.FullLoader)
        cls._config = Config(**config_data)

    @classmethod
    def rethinkdb(cls) -> List[RethinkDBConfig]:
        return cls._config.rethinkdb

    @classmethod
    def redis(cls) -> List[RedisConfig]:
        return cls._config.redis
