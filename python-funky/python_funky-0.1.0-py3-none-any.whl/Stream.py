from typing import Any, Iterable, List

from .generators import *
from .standalone import *


class Stream:

    def __init__(self, iterable: Iterable[Any]):
        self._gen = (x for x in iterable)

    def map(self, fun) -> 'Stream':
        self._gen = generator_map(self._gen, fun)
        return self

    def filter(self, fun) -> 'Stream':
        self._gen = generator_filter(self._gen, fun)
        return self

    def reduce(self, acc, fun) -> Any:
        return reduce(self._gen, acc, fun)

    def as_list(self) -> List[Any]:
        return [x for x in self._gen]

    def as_generator(self) -> Iterable[Any]:
        return self._gen
