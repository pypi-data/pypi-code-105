from typing import Optional, List, Any


def __read_only_properties(*attrs):
    def class_rebuilder(cls):
        "The class decorator"
        class NewClass(cls):
            "This is the overwritten class"
            def __setattr__(self, name, value):
                if name not in attrs:
                    pass
                elif name not in self.__dict__:
                    pass
                else:
                    raise AttributeError("Can't modify {}".format(name))
                super().__setattr__(name, value)
        return NewClass
    return class_rebuilder


@__read_only_properties('files', 'mode')
class Tee:

    def __init__(self, *files: List[str], mode: str = 'w'):
        if mode not in ['w', 'a']:
            raise ValueError(f"Invalid mode '{mode}': select from ['w', 'a']")
        self.files = [open(f, mode) for f in files]
        self.mode = mode

    def __call__(self, *args: Any, sep: Optional[str] = None, end: Optional[str] = None) -> None:
        for f in self.files:
            print(*args, sep=sep, end=end, file=f, flush=True)
        print(*args, sep=sep, end=end)


def tee(*args: Any, sep: Optional[str] = None, end: Optional[str] = None, files: List[str] = [], mode: str = 'w') -> None:
    if mode not in ['w', 'a']:
            raise ValueError(f"Invalid mode '{mode}': select from ['w', 'a']")

    for fname in files:
        with open(fname, mode) as f:
            print(*args, sep=sep, end=end, file=f, flush=True)
    print(*args, sep=sep, end=end)


__all__ = ["Tee", "tee"]
