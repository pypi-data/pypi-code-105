from typing import List

from eyja.db.hub import DataHub
from eyja.utils import now

from .base_data_model import BaseDataModel
from .data_filter import DataFilter


class DataModel(BaseDataModel):
    def __init__(__pydantic_self__, **data) -> None:
        if 'object_id' not in data:
            data.setdefault('object_id', None)
            data.setdefault('created_at', now())
        data.setdefault('updated_at', now())
        super().__init__(**data)

    async def save(__pydantic_self__) -> None:
        __pydantic_self__.updated_at = now()
        await DataHub.save(__pydantic_self__)

    async def delete(__pydantic_self__) -> None:
        await DataHub.delete(__pydantic_self__)

    @property
    def data(self):
        obj_data = self.dict()

        return obj_data

    @classmethod
    async def get(cls, object_id: str) -> 'DataModel':
        return await DataHub.get(cls, object_id)

    @classmethod
    async def find(cls, filter: DataFilter) -> List['DataModel']:
        return await DataHub.find(cls, filter)
