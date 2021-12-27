"""
  Template ref:

    * "${" [ "%" <mod> ] <reference> "}"

    * mod: "first", "join", "sum", "max", "min"

    ${prop[#id:name]}
    ${prop[name]}
    ${opt[@config:domain#name]}
    ${%first prop[#**:test]}
    ${%sum prop[score]}


"""
import typing

from momotor.options.providers import Providers
from momotor.options.parser.reference import resolve_value_reference


def replace_placeholders(
    value: typing.Optional[str], bundles: Providers, *,
    value_processor: typing.Callable[[typing.Optional[str]], str] = None
) -> typing.Optional[str]:
    if not value:
        return value

    assert isinstance(value, str)

    if value_processor is None:
        value_processor = str

    remaining = value
    result = ''

    while '${' in remaining:
        prefix, remaining = remaining.split('${', 1)
        result += prefix

        if prefix.endswith('$'):
            result += '{'
            continue

        value, remaining = resolve_value_reference(remaining, bundles)

        if value is None:
            result += '${'
            continue

        if '}' not in remaining:
            raise ValueError

        garbage, remaining = remaining.split('}', 1)
        if garbage.strip():
            raise ValueError

        result += replace_placeholders(
            value_processor(value), bundles,
            value_processor=value_processor
        )

    result += remaining

    return result
