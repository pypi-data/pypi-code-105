import requests
from .counter import func_count


class HetuModule:
    def __init__(self):
        self.module_id = None
        self._isReady = False
        self._enable_train = False

    @property
    def enable_train(self):
        return self._enable_train

    @property
    def is_ready(self):
        return self._isReady

    @property
    def hyperparamters(self):
        return self._hyperparameters

    def ready(self):
        self._isReady = True

    def infer(self, *args, **kwargs):
        func_count(module_id=self.module_id, func='infer')
        return 1

    def train(self, *args, **kwargs):
        func_count(module_id=self.module_id, func='train')
        return 1

    def change(self):
        raise NotImplementedError
