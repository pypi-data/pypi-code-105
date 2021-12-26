from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional


class Runner(ABC):
    @abstractmethod
    def set_next(self, runner: Runner) -> Runner:
        pass

    @abstractmethod
    def run(self, request) -> Optional[str]:
        pass


class BaseComponent(Runner):
    _next_runner: Runner = None

    def set_next(self, runner: Runner) -> Runner:
        self._next_runner = runner
        return runner

    @abstractmethod
    def run(self, request: Any) -> str:
        if self._next_runner:
            return self._next_runner.run(request)
        return None
