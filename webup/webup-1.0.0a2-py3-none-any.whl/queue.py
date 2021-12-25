from logging import getLogger
from multiprocessing import Queue
from pathlib import Path
from queue import Empty
from typing import List

from webup.cache_control import cache_control
from webup.content_type import content_type
from webup.files import Files
from webup.models import UploadResult
from webup.upload_process import Upload

_logger = getLogger("webup")


def check(queue: "Queue[UploadResult]", timeout: float | None, wip: List[str]) -> None:
    try:
        result = queue.get(block=(timeout is not None), timeout=timeout)
    except Empty:
        return

    wip.remove(result.key)

    if not result.exception:
        _logger.info("%s ~> s3:/%s/%s", result.path, result.bucket, result.key)
        return

    _logger.error(
        "%s ~> s3:/%s/%s",
        result.path,
        result.bucket,
        result.key,
        exc_info=result.exception,
    )
    raise result.exception


def upload(
    dir: str | Path,
    bucket: str,
    concurrent_uploads: int = 8,
    read_only: bool = False,
    region: str | None = None,
) -> None:
    """
    Uploads the local directory `dir` to the S3 bucket `bucket`.

    If `region` is not set then the default region will be used.

    `concurrent_uploads` describes the maximum number of concurrent upload
    threads to allow.

    If `read_only` is truthy then directories will be walked and files will be
    read, but nothing will be uploaded.
    """

    if isinstance(dir, str):
        dir = Path(dir)

    dir = dir.resolve().absolute()

    _logger.debug(
        "Starting %s concurrent %s of %s to %s in %s.",
        concurrent_uploads,
        "read-only uploads" if read_only else "uploads",
        dir,
        bucket,
        region,
    )

    files = Files(dir)
    process_count = 0
    queue: "Queue[UploadResult]" = Queue(concurrent_uploads)
    wip: List[str] = []

    while True:
        full = len(wip) >= concurrent_uploads

        if wip:
            # If we *can* take on more work then don't wait; hurry up and add
            # more threads. Wait only when there's nothing more we can do.
            timeout = 1 if full else None
            check(queue=queue, timeout=timeout, wip=wip)

        if full:
            continue

        if file := files.next:

            wip.append(file.key)

            upload = Upload(
                bucket=bucket,
                cache_control=cache_control(file.path.suffix),
                content_type=content_type(file.path.suffix),
                key=file.key,
                path=file.path.as_posix(),
                queue=queue,
                read_only=read_only,
                region=region,
            )

            upload.start()
            process_count += 1
            continue

        if not wip:
            _logger.debug("No files remaining. Upload complete.")
            return
