from abc import ABC, abstractmethod
from multiprocessing import Process

class Component(ABC, Process):
    @abstractmethod
    def configure(self, config):
        return NotImplemented

    @abstractmethod
    def run(self):
        return NotImplemented

    def __del__(self):
        self.terminate()

class Generator(Component):
    def __init__(self):
        super().__init__()
        self.configure()

    def run(self):
        self.send()

    @abstractmethod
    def send(self):
        return NotImplemented

class Reactor(Component):
    def __init__(self):
        super().__init__()
        self.configure()

    def run(self):
        self.react()

    @abstractmethod
    def react(self):
        return NotImplemented


__all__ = ['Component', 'Generator', 'Reactor']
