import logging
import multiprocessing
import os

__all__ = [
    "get_prefixed_logger",
    "get_file_handler",
    "with_prefix",
    "with_timer"
]


class LockingFileHandler(logging.FileHandler):
    def __init__(self, filename):
        super().__init__(filename)

    def emit(self, record: logging.LogRecord) -> None:
        with multiprocessing.Lock():
            super().emit(record)


def get_file_handler(path: str,
                     fmt: str = "%(asctime)s %(levelname)-5s %(funcName)-26s %(message)s",
                     datefmt: str = "%Y-%m-%d %H:%M:%S",
                     multiprocessing_safe=False) -> logging.FileHandler:
    assert os.path.exists(path)

    formatter = logging.Formatter(fmt)
    formatter.datefmt = datefmt

    cls = LockingFileHandler if multiprocessing_safe else logging.FileHandler
    handler = cls(path)
    handler.setFormatter(formatter)
    return handler


def with_prefix(parent_logger, prefix) -> logging.LoggerAdapter:
    class PrefixAdapter(logging.LoggerAdapter):
        def process(self, msg, kwargs):
            return '%s %s' % (self.extra['prefix'], msg), kwargs

    return PrefixAdapter(parent_logger, {'prefix': prefix})


# legacy name support
get_prefixed_logger = with_prefix


def with_timer(parent_logger) -> logging.LoggerAdapter:
    from commmons import now_seconds

    class TimerAdapter(logging.LoggerAdapter):
        def process(self, msg, kwargs):
            return 'elapsed=%s %s' % (now_seconds() - self.extra['start_time'], msg), kwargs

    return TimerAdapter(parent_logger, {'start_time': now_seconds()})
