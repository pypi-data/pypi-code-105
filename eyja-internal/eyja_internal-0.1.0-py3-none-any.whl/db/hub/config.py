from typing import List

from pydantic import BaseModel

from eyja.db.rethinkdb import RethinkDBConfig
from eyja.errors import LoadConfigError


class Config(BaseModel):
    rethinkdb: List[RethinkDBConfig] = []

    def __init__(self, **data: dict) -> None:
        super().__init__(**data)

        if len(self.rethinkdb) > 1:
            for item in self.rethinkdb:
                if item.name == 'default':
                    raise LoadConfigError('If there is more than one RethinkDB configuration, then each must have a unique name.')
