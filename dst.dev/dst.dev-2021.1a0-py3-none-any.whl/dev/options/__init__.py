from . import coverage, isort, mypy, pep8, pylint, pytest, utils, yapf


def generate_config() -> None:
    pylint.generate_config()
    isort.generate_config()
    yapf.generate_config()
    mypy.generate_config()
    coverage.generate_config()
    pytest.generate_config()
