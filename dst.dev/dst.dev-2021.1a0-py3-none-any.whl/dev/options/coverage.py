from . import utils


CONFIG_FILE = ".coveragerc"
DEFAULTS_BY_SECTION = {
    "run": {},
    "paths": {},
    "report": {
        "exclude_lines": "\n    ".join((
            "",
            r"#\s*(pragma|PRAGMA)[:\s]?\s*(no|NO)\s*(cover|COVER)",
            r"#\s*(coverage)[:\s]?\s*exclude",
            r"^\s*@abstractmethod(\s*\#\s.*)?$",
            r"^\s*(raise NotImplementedError|\.\.\.|pass)(\s*\#\s.*)?$",
        )),
    },
    "html": {},
    "xml": {},
    "json": {},
}


def generate_config() -> None:
    data_by_section = {k: dict(v) for k, v in DEFAULTS_BY_SECTION.items()}
    data_by_section["run"]["omit"] = "\n    ".join((
        "",
        f"{utils.get_package_path()}/tests/*",  # ToDo
        f"{utils.get_package_path()}/cli/*"  # ToDo
    ))

    config = utils.get_config()
    for header in config.sections():
        if header.startswith("coverage:") and header.partition(":")[2] in data_by_section:
            for key, value in config[header].items():
                data_by_section[header.partition(":")[2]][key] = utils.fix_value(value)
    text = "\n\n".join(
        "\n".join((
            f"[{header}]",
            *(f"{k}={v}" for k, v in data.items()),
        )) for header, data in data_by_section.items() if data
    )
    with open(utils.get_file_path(CONFIG_FILE), "wt") as fd:
        fd.write(f"{text}\n")


def parse() -> float:
    with open(f"{utils.get_options()['cache']}/index.html") as fd:
        content = fd.read()
    text = content.partition('<tr class="total">')[2].partition('<td class="right"')[2]
    return float(text.partition(">")[2].partition("%")[0].strip())


def validate():
    score = parse()
    ret = f"Coverage score: {score:.2f}%"
    if score < utils.get_options()["coverage-minimum"]:
        raise ValueError(f"{ret} < {utils.get_options()['coverage-minimum']:.2f}%")
    return ret
