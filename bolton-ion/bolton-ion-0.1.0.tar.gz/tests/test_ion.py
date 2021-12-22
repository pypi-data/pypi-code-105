"""Tests for the ion package."""

from __future__ import annotations

from _pytest.monkeypatch import MonkeyPatch

import ion


def test_confirm(monkeypatch: MonkeyPatch) -> None:
    """Test the ion.confirm() function."""
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert ion.confirm("test prompt")
