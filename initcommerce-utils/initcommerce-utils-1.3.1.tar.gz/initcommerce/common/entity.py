import abc
from typing import Optional

from pydantic import (  # noqa: F401
    BaseConfig,
    BaseModel,
    Field,
    root_validator,
    validator,
)


class BaseEntity(BaseModel, metaclass=abc.ABCMeta):
    id: Optional[int]

    class Config(BaseConfig):
        orm_mode = True
