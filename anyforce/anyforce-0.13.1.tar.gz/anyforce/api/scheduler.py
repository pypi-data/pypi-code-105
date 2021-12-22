from datetime import datetime
from typing import Any, Callable, Dict, Generic, Optional, Protocol

from dateutil.parser import parse
from fastapi import Request
from tortoise import Tortoise

from ..asyncio import coro
from ..model import BaseModel
from .api import Model, UpdateForm, UserModel


class Worker(Protocol):
    def enqueue_at(
        self, at: datetime, f: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> Any:
        raise NotImplementedError()


@coro
async def update(app: str, name: str, q: Dict[str, Any], form: Dict[str, Any]):
    model = Tortoise.apps[app][name]
    obj = await model.filter(**{k: v for k, v in q.items()}).get()
    assert isinstance(obj, BaseModel)
    obj.update(form)
    await obj.save()


class Scheduler(Generic[UserModel, Model, UpdateForm]):
    def __init__(self, worker: Worker) -> None:
        super().__init__()
        self.worker = worker

    async def before_update(
        self, user: UserModel, obj: Model, input: UpdateForm, request: Request
    ) -> Optional[Model]:
        schedule_at = request.query_params.get("schedule_update_at")

        if schedule_at:
            schedule_at = parse(schedule_at)
            assert isinstance(schedule_at, datetime)
            schedule_at = schedule_at.astimezone()

            v = input.dict(exclude_unset=True)
            assert v

            meta = obj.__class__._meta  # type: ignore
            pk_attr = meta.pk_attr
            pk_v = v.pop(pk_attr, None)
            assert pk_v

            self.worker.enqueue_at(
                schedule_at,
                update,
                app=meta.app,
                name=obj.__class__.__name__,
                q={pk_attr: pk_v},
                form=v,
            )
            return None
        return obj
