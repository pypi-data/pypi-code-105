from abc import ABC, abstractmethod
from threading import Thread

class Worker(ABC, Thread):
    @abstractmethod
    def configure(self, config):
        return NotImplemented

    @abstractmethod
    def work(self):
        return NotImplemented

    def run(self):
        self.work()

    def __init__(self, config):
        super().__init__()
        self.configure(config)

    def __del__(self):
        self.terminate()

__all__ = ['Worker']
