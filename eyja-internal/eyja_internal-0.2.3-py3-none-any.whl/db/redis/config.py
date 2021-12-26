from typing import List

from pydantic import BaseModel


class RedisConfig(BaseModel):
    name: str = 'default'
    host: str = 'localhost'
    port: int = 6379
    db: dict = {}
