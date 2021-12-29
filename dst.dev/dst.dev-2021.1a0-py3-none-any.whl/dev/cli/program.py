import os
import sys
from contextlib import suppress
from functools import wraps

import pylint_json2html
from coverage.config import CoverageConfig
from mypy.__main__ import console_entry as run_mypy
from pylint import run_pylint
from isort.main import main as run_isort
from pycodestyle import _main as run_pep8
from yapf import run_main as run_yapf
from pytest import console_main as run_pytest

from dst.dev import options


def pep8(args=()):
    config = options.utils.get_config()

    data = dict(options.pep8.DEFAULTS)
    if "pycodestyle" in config:
        for key in data:
            if key in config["pycodestyle"]:
                data.pop(key)

    sys.argv = [
        sys.argv[0],
        options.utils.get_package_path(),
        *(f"--{k.replace('_', '-')}{f'={v}' if v is not True else ''}" for k, v in data.items() if v is not False),
        *args,
    ]
    run_pep8()


def pylint(args=(), *, as_error=False):
    sys.argv = [
        sys.argv[0],
        options.utils.get_package_path(),
        "--load-plugins=pylint_json2html",
        "--output-format=jsonextended",
        f"--output={options.utils.get_options()['cache']}/pylint.json",
        *args,
    ]
    with suppress(SystemExit):
        run_pylint()
    sys.argv = [
        sys.argv[0],
        f"{options.utils.get_options()['cache']}/pylint.json",
        "--input-format=jsonextended",
        f"--output={options.utils.get_options()['cache']}/pylint.html",
    ]
    pylint_json2html.main()
    sys.argv = [
        sys.argv[0],
        options.utils.get_package_path(),
        *args,
    ]
    with suppress(SystemExit):
        run_pylint()
    print(f"Pylint report: file://{os.getcwd()}/{options.utils.get_options()['cache']}/pylint.html")
    try:
        print(options.pylint.validate())
    except ValueError as e:
        if as_error:
            raise
        print(e)
        sys.exit(1)


def isort(args=(), *, modify=False):
    if not modify:
        args = ["--check-only", *args]
    sys.argv = [sys.argv[0], f"{options.utils.get_package_path()}/", *args]
    run_isort()


def yapf(args=(), *, modify=False):
    exclude = []
    with suppress(KeyError):
        exclude = options.utils.get_config(options.yapf.CONFIG_FILE)["dst.dev"]["exclude"].split("\n")
    sys.argv = [
        sys.argv[0],
        *(
            os.path.join(directory_path, filename)
            for directory_path, _, filenames in os.walk(options.utils.get_package_path())
            for filename in filenames
            if (filename.endswith(".py") or filename.endswith(".pyi")) and not any(
                os.path.join(directory_path, filename).startswith(f"{exclude_start.strip('/')}/")
                for exclude_start in filter(None, exclude)
            )
        ),
        "--in-place" if modify else "--diff",
        *args,
    ]
    run_yapf()


def mypy(args=()):
    sys.argv = [sys.argv[0], options.utils.get_package_path(), *args]
    run_mypy()


def pytest(args=(), *, as_error=False):

    @wraps(CoverageConfig.post_process)
    def post_process(self: CoverageConfig):
        if self.data_file == ".coverage":
            self.data_file = f"{options.utils.get_options()['cache']}/.coverage"
        _post_process(self)

    _post_process, CoverageConfig.post_process = CoverageConfig.post_process, post_process

    tests = options.utils.get_options()["tests"]
    if not os.path.exists(tests):
        tests = f"{options.utils.get_package_path()}/{tests}"
    sys.argv = [sys.argv[0], tests, *args]
    run_pytest()
    print(f"Pytest report: file://{os.getcwd()}/{options.utils.get_options()['cache']}/report.html")
    print(f"Coverage report: file://{os.getcwd()}/{options.utils.get_options()['cache']}/index.html")
    try:
        print(options.pytest.validate())
        print(options.coverage.validate())
    except ValueError as e:
        if as_error:
            raise
        print(e)
        sys.exit(1)


def build():
    ...

# build-dist:
# 	@echo
# 	@( \
# 		. $(ENV_NAME)/bin/activate; \
# 		python setup.py sdist bdist_wheel; \
# 	)
# 	@echo
#
#
# twine-check:
# 	@echo
# 	@( \
# 		. $(ENV_NAME)/bin/activate; \
# 		twine check dist/* ; \
# 	)
# 	@echo
