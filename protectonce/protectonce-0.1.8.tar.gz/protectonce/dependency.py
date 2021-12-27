import json
from logging import raiseExceptions


class Dependency(json.JSONEncoder):
    def __init__(self, name, version, vendor, type):
        self.name = name
        self.version = version
        self.vendor = vendor
        self.type = type

    def __repr__(self):
        return (
            '{"name":"%s",' % self.name
            + '"vendor":"%s",' % self.vendor
            + '"version":"%s",' % self.version
            + '"type":"%s"}' % self.type
        )


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        return str(o) if isinstance(o, Dependency) else super().default(o)
