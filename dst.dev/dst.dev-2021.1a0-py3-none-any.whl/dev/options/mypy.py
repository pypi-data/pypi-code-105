import mypy.defaults

from . import utils


CONFIG_FILE = mypy.defaults.CONFIG_FILE[-1]
DEFAULTS = {
    "ignore_missing_imports": "True",
}


def generate_config() -> None:
    config = utils.get_config()
    data = dict(DEFAULTS, cache_dir=f"{utils.get_options()['cache']}/{mypy.defaults.CACHE_DIR}")

    data["exclude"] = "\n    ".join(
        (f"{utils.get_package_path()}/{key}" for key in utils.get_options()["mypy-exclude"])
    )
    if config["options"].get("namespace_packages"):
        data["namespace_packages"] = "True"
        data["explicit_package_bases"] = "True"

    for header in config.sections():
        if header == "mypy":
            for key, value in config[header].items():
                data[key] = utils.fix_value(value)
    text = "\n".join(f"{k}={v}" for k, v in data.items())
    with open(utils.get_file_path(CONFIG_FILE), "wt") as fd:
        fd.write(f"[mypy]\n{text}\n")
        for header in config.sections():
            if header.startswith("mypy-") and config[header]:
                fd.write(f"\n[{header}]\n")
                for key, value in config[header].items():
                    fd.write(f"{key}={value}\n")
