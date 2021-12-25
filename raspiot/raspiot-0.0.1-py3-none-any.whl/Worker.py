from abc import ABC, abstractmethod
from multiprocessing import Process

class Worker(ABC, Process):
    @abstractmethod
    def configure(self, config):
        return NotImplemented

    @abstractmethod
    def work(self):
        return NotImplemented

    def run(self):
        self.work()

    def __init__(self, config):
        self.configure(config)

    def __del__(self):
        self.terminate()

__all__ = ['Worker']
