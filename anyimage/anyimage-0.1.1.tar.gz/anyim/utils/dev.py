"""A collection of aws tools"""
import os

import fire


PYLINT_MESSAGE_TYPES = ["R", "C", "E", "W"]

ENCHANT_ADDITIONAL_VOCAB = [
    "Args",
    "str",
    "env",
    "config",
    "emr",
    "datetime",
    "bool",
    "args",
    "kwargs",
    "wr",
    "configs",
    "aws",
    "pyspark",
    "pwd",
    "cmd",
    "dockerfile",
    "ipykernel",
    "IPython",
    "sys",
    "sql",
    "Dataframe",
    "pyemr",
    "DataFrame",
    "toml",
    "pyproject",
    "awswrangler",
    "gitignore",
    "stdout",
    "stderr",
    "pypi",
    "formatter",
    "smm",
]


def format_code():
    """Runs a series of python code format converts on the code in the working directory."""
    os.system("pyment --output=google --write .")

    os.system(
        "autoflake --in-place --remove-unused-variables --remove-all-unused-imports **/*.py",
    )
    os.system("autopep8 --in-place **/*.py")
    os.system("black .")
    os.system("isort .")
    os.system("brunette **/*.py")
    os.system("gray *")


def lint_wd(spelling=False, *args, **kwargs):
    """Runs pylint on the pwd.

    Args:
      *args:
      **kwargs:
      spelling: (Default value = False)

    Returns:

    """
    if "S" not in kwargs:
        args = " ".join(args)
        kwargs = " ".join([f"-{k} {v}" for k, v in kwargs.items()])
        cmd = ["pylint", "--ignore", "HOWTO.md,README.md,poetry.lock,pyproject.toml"]
        if args:
            cmd += [args]
        if kwargs:
            cmd += [kwargs]

        cmd += ["*"]
        os.system(" ".join(cmd))
    else:
        cmd = ["pylint"]
        cmd += ["--disable", "all", "--enable", "spelling", "--spelling-dict", "en_US"]
        cmd += ["--spelling-ignore-words", ",".join(ENCHANT_ADDITIONAL_VOCAB)]
        cmd += ["*"]
        os.system(" ".join(cmd))


if __name__ == "__main__":
    fire.Fire(format_code)
