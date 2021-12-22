"""Tests for the typist package."""

from __future__ import annotations

from typing import List, Literal, cast

import pytest
from pytest import mark

from typist import assert_never, literal_to_list


params = mark.parametrize

Animal = Literal["cat", "dog", "pig"]


def test_literal_to_list() -> None:
    """Test the literal_to_list() function."""
    assert literal_to_list(Animal) == ["cat", "dog", "pig"]


def test_assert_never() -> None:
    """Test the assert_never() function.

    NOTE: CI's lint checks also play a role in testing the code in this test
      function. The '# type: ignore' pragmas, in particular, will cause mypy to
      fail if the assert_never() funciton is not right.
    """
    bad_animals = literal_to_list(Animal) + ["unicorn"]

    # bad cast to List[Animal]
    for a1 in cast(List[Animal], bad_animals):
        if a1 == "cat":
            print("cat")
        elif a1 == "dog":
            print("dog")
        elif a1 == "pig":
            print("pig")
        else:
            with pytest.raises(AssertionError):  # type: ignore[unreachable]
                assert_never(a1)

    # no cast (real type)
    for a2 in bad_animals:
        if a2 == "cat":
            print("cat")
        elif a2 == "dog":
            print("dog")
        elif a2 == "pig":
            print("pig")
        else:
            with pytest.raises(AssertionError):
                assert_never(a2)  # type: ignore[arg-type]
