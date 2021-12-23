from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from rq import Queue
from rq.job import Job as RQJOb
from rq.registry import ScheduledJobRegistry

from .typing import Job, Status
from .typing import Worker as WorkerProtocol


class Worker(object):
    def __init__(self, queue: Queue) -> None:
        super().__init__()
        self.queue = queue
        self.registry = ScheduledJobRegistry(
            self.queue.name,
            connection=self.queue.connection,
            serializer=self.queue.serializer,
        )

    def _(self) -> WorkerProtocol:
        return self

    def enqueue_at(
        self, datetime: datetime, f: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> Any:
        return self.queue.enqueue_at(datetime, f, *args, **kwargs)

    def list(
        self, offset: int, limit: int, condition: Optional[Dict[str, str]] = None
    ) -> List[Job]:
        jobs: List[Job] = []
        while True:
            job_ids = self.registry.get_job_ids(offset, offset + limit)
            offset += limit
            if len(job_ids) < limit:
                return jobs

            rq_jobs: List[RQJOb] = RQJOb.fetch_many(
                job_ids,
                connection=self.queue.connection,
                serializer=self.queue.serializer,
            )
            for job in rq_jobs:
                kwargs = job.kwargs.copy()
                context: Dict[str, str] = kwargs.pop("context", {})
                if condition:
                    if any(
                        [context.get(k, "").find(v) < 0 for k, v in condition.items()]
                    ):
                        continue

                status = Status.t(Status.pending)
                if job.is_finished:
                    status = Status.t(Status.finished)
                elif job.is_failed:
                    status = Status.t(Status.failed)
                elif job.is_canceled or job.is_stopped:
                    status = Status.t(Status.canceled)

                jobs.append(
                    Job(
                        id=job.id,
                        status=status,
                        args=job.args,
                        kwargs=kwargs,
                        context=context,
                        result=str(job.result),
                    )
                )
                if len(jobs) >= limit:
                    return jobs

    def cancel(self, job: Job) -> Any:
        rq_job = RQJOb.fetch(
            job.id, connection=self.queue.connection, serializer=self.queue.serializer
        )
        return rq_job.cancel()
