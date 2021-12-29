import importlib
import sys
import tempfile
from contextlib import suppress

import pylint.lint

from . import utils


CONFIG_FILE = ".pylintrc"
DEFAULTS = {
    "reports": "yes",
    "max-line-length": "120",
    "valid-metaclass-classmethod-first-arg": "mcs",
    "ignore-imports": "yes",
}
EXTEND = {
    "enable": ["useless-suppression"],
    "disable": ["unspecified-encoding"],
    "property-classes": ["cached_property"],
    "good-names": [
        "e",  # error
        "f",  # function, and others
        "i",  # index/iteration
        "j",  # secondary index/iteration
        "k",  # key
        "v",  # value
        "x",  # item
        "y",  # other item
        "z",  # third item
        "cm",  # context manager
        "fd",  # file descriptor
    ],
}
with suppress(ModuleNotFoundError):
    importlib.import_module("pandas")
    EXTEND["good-names"].append("df")  # DataFrame
with suppress(ModuleNotFoundError):
    importlib.import_module("django")
    EXTEND["good-names"].extend(["q", "qs"])  # Q, QuerySet


def generate_config() -> None:
    config = utils.get_config()

    defaults = dict(DEFAULTS)
    extend = {k: [*v] for k, v in EXTEND.items()}
    for header in config.sections():
        if header.partition(":")[0] == "pylint":
            for key in {*defaults}.intersection(config[header]):
                defaults.pop(key)
            for key in {*extend}.intersection(config[header]):
                extend[key].extend(
                    x.strip() for x in config[header][key].split(",") if x.strip() and x.strip() not in extend[key]
                )

    with tempfile.NamedTemporaryFile() as temp_file:
        sys.argv = [
            sys.argv[0],
            "--generate-rcfile",
            f"--rcfile={utils.get_file_path(utils.CONFIG_FILE)}",
        ]
        with open(temp_file.name, "wt") as fd:
            stdout, sys.stdout = sys.stdout, fd
            with suppress(SystemExit):
                pylint.run_pylint()
            sys.stdout = stdout
        with open(temp_file.name, "rt") as fd:
            text = fd.read()

    defaults = {
        **defaults,
        **{k: f",\n{' ' * len(k)} ".join(v) for k, v in extend.items()},
    }
    for key, value in defaults.items():
        start, _, end = text.partition(f"\n{key}=")
        end = end.partition("\n\n")[2]
        text = f"{start}\n{key}={value}\n\n{end}"

    with open(utils.get_file_path(CONFIG_FILE), "wt") as fd:
        fd.write(text)


def parse() -> float:
    with open(f"{utils.get_options()['cache']}/pylint.html") as fd:
        content = fd.read()
    text = content.partition("<h2>Score</h2>")[2]
    return float(text.partition("/")[0].strip()) * 10


def validate():
    score = parse()
    ret = f"Pylint score: {score:.2f}%"
    if score < utils.get_options()["pylint-minimum"]:
        raise ValueError(f"{ret} < {utils.get_options()['pylint-minimum']:.2f}%")
    return ret
