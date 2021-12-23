from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Protocol

from pydantic import BaseModel, Field

from ...model.enum import StrEnum


class Status(StrEnum):
    pending = "pending", "等待"
    failed = "failed", "失败"
    finished = "finished", "完成"
    canceled = "canceled", "取消"


class Job(BaseModel):
    id: str
    status: Status = Status.t(Status.pending)
    title: str = ""
    args: List[Any] = Field(default_factory=list)
    kwargs: Dict[str, Any] = Field(default_factory=dict)
    context: Dict[str, str] = Field(default_factory=dict)


class Worker(Protocol):
    def enqueue_at(
        self, datetime: datetime, f: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> Any:
        raise NotImplementedError()

    def list(
        self, offset: int, limit: int, condition: Optional[Dict[str, str]]
    ) -> List[Job]:
        raise NotImplementedError()

    def cancel(self, job: Job) -> Any:
        raise NotImplementedError()
