from typing import List

from pydantic import BaseModel

from eyja.db.rethinkdb import RethinkDBConfig
from eyja.db.redis import RedisConfig
from eyja.errors import LoadConfigError


class Config(BaseModel):
    rethinkdb: List[RethinkDBConfig] = []
    redis: List[RedisConfig] = []

    def __init__(self, **data: dict) -> None:
        super().__init__(**data)

        if len(list(filter(lambda item: item.name == 'default', self.rethinkdb))) > 1:
            raise LoadConfigError('If there is more than one RethinkDB configuration, then each must have a unique name.')

        if len(list(filter(lambda item: item.name == 'default', self.redis))) > 1:
            raise LoadConfigError('If there is more than one Redis configuration, then each must have a unique name.')