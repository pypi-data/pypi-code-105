import isort.main

from . import utils


CONFIG_FILE = isort.settings.CONFIG_SOURCES[0]
DEFAULTS = {
    "include_trailing_comma": "True",
    "lines_after_imports": "2",
    "multi_line_output": "VERTICAL_HANGING_INDENT",
}


def generate_config() -> None:
    config = utils.get_config()
    data = dict(DEFAULTS)
    data["known_first_party"] = config["metadata"]["name"]
    data["skip"] = "\n    ".join((f"{utils.get_package_path()}/{key}" for key in utils.get_options()["isort-exclude"]))
    for header in config.sections():
        if header in isort.settings.CONFIG_SECTIONS[utils.CONFIG_FILE]:
            for key, value in config[header].items():
                data[key] = utils.fix_value(value)
    text = "\n".join(f"{k}={v}" for k, v in data.items())
    with open(utils.get_file_path(CONFIG_FILE), "wt") as fd:
        fd.write(f"[settings]\n{text}\n")
