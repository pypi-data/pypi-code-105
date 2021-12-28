from typing import Callable, Any

class _StateManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(_StateManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.state = {}
        self.subscriber = {}

    def set(self, key, value):
        self.state[key] = value
        for callback in self.subscriber:
            callback(value)

    def subscribe(self, key, callback):
        self.subscriber[key] = callback

    # TODO: unused
    def get(self, key):
        return self.state[key]

    # TODO: unused
    def delete(self, key):
        del self.state[key]

    # TODO: unused
    def clear(self):
        self.state = {}

class Pipeline:
    def __init__(self):
        self.manager = _StateManager()

    def publish(self, name: str, state) -> None:
        self.manager.set(name, state)

    def subscribe(self, name: str, callback: Callable[[Any], None]) -> None:
        self.manager.subscribe(name, callback)

__all__ = ['Pipeline']
