import configparser
import importlib
import os
from contextlib import suppress


CONFIG_FILE = "setup.cfg"
SECTION = "dst.dev"
DEFAULTS = {
    "cache": ".tests",
    "tests": "tests",
    "pytest-maxfailed": 0,
    "pytest-maxskipped": 0,
    "pylint-minimum": 100.0,
    "coverage-minimum": 100.0,
    "mypy-exclude": ["tests"],
    "isort-exclude": [],
    "yapf-exclude": [],
    "pylint-exclude": [],
    "coverage-exclude": [],
}
with suppress(ModuleNotFoundError):
    importlib.import_module("django")
    DEFAULTS["mypy-exclude"].append("migrations")
    DEFAULTS["isort-exclude"].append("migrations")
    DEFAULTS["yapf-exclude"].append("migrations")
    DEFAULTS["pylint-exclude"].append("migrations")
for k in [*DEFAULTS]:
    if k.endswith("-exclude"):
        DEFAULTS[f"{k[:-len('-exclude')]}-include"] = []


def get_file_path(filename: str, directory: str = None) -> str:
    if directory is None:
        return filename
    directory = os.path.expanduser(directory)
    return os.path.join(directory, filename)


def get_config(filename: str = CONFIG_FILE) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    assert config.read(get_file_path(filename))
    return config


def get_package_path(filename: str = CONFIG_FILE, *, full: bool = False) -> str:
    config = get_config(filename)
    module_path = importlib.import_module(config["metadata"]["name"]).__path__[0]
    assert module_path.startswith(f"{os.getcwd()}/"), module_path
    if full:
        return module_path.strip("/")
    return module_path[len(f'{os.getcwd()}/'):].strip("/")  # ToDo .removeprefix


def fix_value(value: str) -> str:
    if "\n" in value:
        return "\n    " + value.strip().replace("\n", "\n    ")
    return value


def get_options(filename: str = CONFIG_FILE):
    config = get_config(filename)
    data = dict(DEFAULTS)
    if SECTION not in config:
        return data
    for key in config[SECTION]:
        assert key in data  # ToDo assert bad
        if isinstance(data[key], bool):
            data[key] = config[SECTION].getboolean(key)
        elif isinstance(data[key], list):
            values = "\n".join(config[SECTION][key].split(",")).split("\n")
            data[key].extend(x.strip() for x in values if x not in data[key])
        elif isinstance(data[key], float):
            data[key] = config[SECTION].getfloat(key)
        elif isinstance(data[key], int):
            data[key] = config[SECTION].getint(key)
        else:
            assert isinstance(data[key], str)
            data[key] = config[SECTION][key]
    for key, value in data.items():
        if key.endswith("-include"):
            key_exclude = f"{key[:-len('-include')]}-exclude"
            data[key_exclude] = [x for x in data[key_exclude] if x not in value]
    return data
