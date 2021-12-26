# internal
import abc
from contextlib import contextmanager


class Agent(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def act(self, *args, **kwargs):
        pass

    @contextmanager
    def evaluate(self):
        try:
            yield
        finally:
            pass
