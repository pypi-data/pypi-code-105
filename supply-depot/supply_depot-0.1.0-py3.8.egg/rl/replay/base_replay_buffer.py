import abc
from typing import Any


class BaseReplayBuffer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def sample(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def append(self, sample: Any):
        pass

    @abc.abstractmethod
    def remove(self, idx: int):
        pass
