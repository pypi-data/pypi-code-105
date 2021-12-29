from typing import Tuple

from . import utils


CONFIG_FILE = "pytest.ini"
DEFAULTS = {
    "log_cli_level": "INFO",
}


def generate_config() -> None:
    config = utils.get_config()
    data = dict(
        DEFAULTS,
        cache_dir=f"{utils.get_options()['cache']}/.pytest_cache",
        addopts=(
            "--tb=native "
            f"--html={utils.get_options()['cache']}/report.html "
            f"--cov {config['metadata']['name']} "
            "--cov-report term-missing "
            f"--cov-report html:{utils.get_options()['cache']}"
        )
    )

    for header in config.sections():
        if header == "tool:pytest":
            for key, value in config[header].items():
                data[key] = utils.fix_value(value)

    text = "\n".join(f"{k}={v}" for k, v in data.items())
    with open(utils.get_file_path(CONFIG_FILE), "wt") as fd:
        fd.write(f"[pytest]\n{text}\n")


def parse() -> Tuple[int, int]:
    with open(f"{utils.get_options()['cache']}/report.html") as fd:
        content = fd.read()

    failed_text = content.partition("<span class=\"failed\">")[2].partition("</span>")[0]
    assert failed_text.endswith(" failed"), failed_text
    failed = int(failed_text.rpartition(" ")[0])

    skipped_text = content.partition("<span class=\"skipped\">")[2].partition("</span>")[0]
    assert skipped_text.endswith(" skipped"), skipped_text
    skipped = int(skipped_text.rpartition(" ")[0])

    return failed, skipped


def validate():
    failed, skipped = parse()
    ret = f"{failed} failed, {skipped} skipped"
    if failed > utils.get_options()["pytest-maxfailed"]:
        raise ValueError(f"{ret}; expected not more than {utils.get_options()['pytest-maxfailed']!r} failed tests")
    if skipped > utils.get_options()["pytest-maxskipped"]:
        raise ValueError(f"{ret}; expected not more than {utils.get_options()['pytest-maxskipped']!r} skipped tests")
    return ret
