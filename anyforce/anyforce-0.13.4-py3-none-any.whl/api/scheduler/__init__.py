from datetime import datetime
from typing import Any, Callable, Coroutine, Dict, List, Optional, Union, cast

from dateutil.parser import parse
from fastapi import Query, Request
from fastapi.param_functions import Depends
from fastapi.responses import ORJSONResponse
from fastapi.routing import APIRouter
from pydantic import BaseModel as PydanticBaseModel
from tortoise import Tortoise

from ...asyncio import coro
from ...json import loads
from ...logging import getLogger
from ...model import BaseModel
from ..api import Model
from .typing import Job, Worker

logger = getLogger(__name__)


@coro
async def update(
    app: str,
    name: str,
    q: Dict[str, Any],
    form: Dict[str, Any],
    context: Dict[str, str],
):
    logger.with_field(context=context).info("update")
    model = Tortoise.apps[app][name]
    obj = await model.filter(**{k: v for k, v in q.items()}).get()
    assert isinstance(obj, BaseModel)
    obj.update(form)
    await obj.save()


class Scheduler(object):
    def __init__(
        self,
        worker: Worker,
        schedule_update_at_key: str = "schedule_update_at",
        context_keys: List[str] = [],
    ) -> None:
        super().__init__()
        self.worker = worker
        self.schedule_update_at_key = schedule_update_at_key
        self.context_keys = context_keys

    def bind(
        self,
        router: APIRouter,
        depend: Callable[..., Union[Coroutine[Any, Any, Any], Any]],
    ):
        @router.get("/", response_class=ORJSONResponse)
        def list(
            offset: int = Query(0, title="分页偏移"),
            limit: int = Query(20, title="分页限额"),
            condition: str = Query(
                [], title="查询条件", description='{ "{context_k}": "v" }'
            ),
            _: Any = Depends(depend),
        ) -> List[Job]:
            return self.worker.list(
                offset, limit, cast(Dict[str, str], loads(condition))
            )

        return list

    def before_update(
        self,
        obj: Model,
        input: PydanticBaseModel,
        request: Request,
        name_key: str = "name",
    ) -> Optional[Model]:
        schedule_at = request.query_params.get(self.schedule_update_at_key)

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

            context: Dict[str, str] = {"name": getattr(obj, name_key, str(pk_v))}
            for key in self.context_keys:
                context[key] = request.query_params.get(key, "")

            self.worker.enqueue_at(
                schedule_at,
                update,
                app=meta.app,
                name=obj.__class__.__name__,
                q={pk_attr: pk_v},
                form=v,
                context=context,
            )
            return None
        return obj
