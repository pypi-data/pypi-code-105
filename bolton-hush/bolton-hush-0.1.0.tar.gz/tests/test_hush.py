"""Tests for the hush package."""

from __future__ import annotations

from hush import Hush, get_secret

from .conftest import FOO


def test_get_secret__ENVVAR(mock_envvars: None) -> None:
    """Test the get_secret() function with environment variables."""
    del mock_envvars

    secret = get_secret("foo")
    assert secret == FOO

    hush = Hush(["path", "to"])
    assert hush.get_secret("foo") == FOO
