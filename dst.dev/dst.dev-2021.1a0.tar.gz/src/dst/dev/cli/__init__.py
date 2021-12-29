import sys

from dst.dev import options
from . import program


def main():
    _, *args = sys.argv
    if not args:
        args = ["-h"]
    name, *args = args
    if name == "-h":
        print("    dst.dev generate")
        print("    dst.dev run pep8")
        print("    dst.dev run isort")
        print("    dst.dev run yapf")
        print("    dst.dev run pylint (--raise)")
        print("    dst.dev run mypy")
        print("    dst.dev run pytest (--raise)")
        print("    dst.dev modify isort")
        print("    dst.dev modify yapf")
    elif name == "generate":
        assert not args
        options.generate_config()
        print(f"`dst.dev {name}` ok")
    else:
        kwargs = {}
        if name == "modify":
            kwargs[name] = True
        elif name != "run":
            raise LookupError(name, *args)
        target, *args = args
        if "--raise" in args:
            kwargs["as_error"] = True
            args = [x for x in args if x != "--raise"]
        getattr(program, target)(args, **kwargs)
        print(f"`dst.dev {name} {target}` ok")
