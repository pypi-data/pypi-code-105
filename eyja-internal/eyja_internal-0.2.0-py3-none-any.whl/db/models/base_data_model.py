from datetime import datetime

from pydantic import BaseModel

from .base_internal import BaseInternal


class BaseDataModel(BaseModel):
    class Internal(BaseInternal):
        pass

    object_id: str = None
    created_at: datetime
    updated_at: datetime

