import os


class RootPath:
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead.')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls.path = os.path.dirname(__file__)
            cls.cwd = os.getcwd()
        return cls._instance
