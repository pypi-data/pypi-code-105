from typing import Dict

from webup.suffix import normalize_suffix

_max_ages: Dict[str, int] = {}

_default_max_age = -1


def set_default_maximum_age(seconds: int = 60) -> None:
    """
    Sets the Cache-Control "max-age" value for files not registered via
    `set_maximum_age`.

    Defaults to 60 seconds.
    """

    global _default_max_age
    _default_max_age = seconds


def cache_control(suffix: str) -> str:
    """
    Gets the Cache-Control header for a type of file.

    Arguments:
        suffix: Filename suffix.
    """

    return f"max-age={max_age(suffix)}"


def max_age(suffix: str) -> int:
    """
    Gets the maximum age in seconds for a type of file.

    Arguments:
        suffix: Filename suffix.
    """

    suffix = normalize_suffix(suffix)
    return _max_ages.get(suffix, _default_max_age)


def set_maximum_age(suffix: str, seconds: int) -> None:
    """
    Sets the "max-age" value of the Cache-Control header for files with the
    `suffix` filename extension.

    There are no per-suffix ages set by default.
    """

    suffix = normalize_suffix(suffix)
    _max_ages[suffix] = seconds


set_default_maximum_age()
