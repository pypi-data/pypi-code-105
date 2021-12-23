"""This file contains shared fixtures and pytest hooks.

https://docs.pytest.org/en/6.2.x/fixture.html#conftest-py-sharing-fixtures-across-multiple-files
"""

import os
from typing import Iterator
from unittest.mock import patch

from pytest import fixture


FOO = "FOOOO"


@fixture
def mock_envvars() -> Iterator[None]:
    """Mocks needed to test environment variable secrets."""
    with patch.dict(os.environ, {"FOO": FOO, "PATH_TO_FOO": FOO}):
        yield
