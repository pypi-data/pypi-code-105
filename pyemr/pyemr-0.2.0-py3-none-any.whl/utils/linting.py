"""A collection of aws tools"""
import os
from spellcheck import SpellCheck
from autocorrect import spell

import fire

def spell_check(path):
    with open(path,'r') as file:
        text = file.read()
    
    for work in

    

def format_code():
    """Runs python reformaters on the pwd."""
    os.system("pyment --output=google --write .")

    os.system(
        "autoflake --in-place --remove-unused-variables --remove-all-unused-imports **/*.py",
    )
    os.system("autopep8 --in-place **/*.py")
    os.system("black .")
    os.system("isort .")
    os.system("brunette **/*.py")
    os.system("gray *")


PYLINT_MESSAGE_TYPES = ["R", "C", "E", "W"]


def lint_wd(*args, **kwargs):
    """Runs pylint on the pwd.

    Args:
      *args:
      **kwargs:

    Returns:

    """
    args = " ".join(args)
    kwargs = " ".join([f"-{k} {v}" for k, v in kwargs.items()])
    cmd = ["pylint","--ignore", "HOWTO.md,README.md,poetry.lock,pyproject.toml"]
    if args:
        cmd += [args]
    if kwargs:
        cmd += [kwargs]
    cmd += ["*"]
    os.system(" ".join(cmd))


if __name__ == "__main__":
    fire.Fire(format_code)
