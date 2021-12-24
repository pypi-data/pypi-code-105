from typing import Any
from pathlib import Path


def leading_spaces(line: str) -> int:
    """
    Calculates the number of leading spaces in a string.

    Parameters
    ----------
    line

    Returns
    -------
    int
    """
    return len(line) - len(line.lstrip())


def parse_value(value: str) -> Any:
    """
    Parses a value into its proper type.

    Parameters
    ----------
    value: str

    Returns
    -------
    Any
    """
    value = value.strip()
    if value.isdigit():
        return int(value)
    try:
        return float(value)
    except ValueError:
        pass
    if value.lower() in ['true', 'false']:
        return value.lower() == 'true'
    if value.lower() in ['none', 'null']:
        return None
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        value = value[1:-1]
    if '~' in value:
        value = str(Path(value).expanduser())
    return value


def parse_line(line: str, sep: str = '=') -> tuple[str, Any] | None:
    """
    Parses a line into a key and value.

    Examples
    --------
    `key = value`
    `key: value`

    Parameters
    ----------
    line: str
    sep: str
        The separator for splitting

    Returns
    -------
    Tuple[str, Any]
        The key and value of the line.
    """
    if line.startswith('#'):
        return None
    if sep not in line:
        return None
    key, value = line.split(sep, 1)
    value: Any = parse_value(value)
    return key, value
