"""
    [ "%" <mod> ] <reference> [ <oper> [ <value> ] ]

    * mod: "any" (one must match), "all" (all must match), "not" (at least one must not match), "none" (none must match)
    * outcome: "pass", "fail", "error", "skip"

    pass
    prop[#test]?
    prop[#test]>0
    %any prop[#test]>0
    %any fail
    %none pass
    %not pass[#test.$0]

"""
import collections
import typing

from momotor.bundles.elements.base import Element
from momotor.options.parser.modifier import parse_mod
from momotor.options.parser.reference import parse_reference, match_reference, Reference
from momotor.options.parser.consts import VALUE_ATTR, OPERATIONS, OPERATIONS_WITHOUT_VALUE, CONDITION_RE
from momotor.options.providers import Providers
from momotor.options.task_id import StepTaskId


def parse_selector(selector: str, task_id: typing.Optional[StepTaskId]) \
        -> typing.Tuple[
            typing.Optional[str],
            str,
            typing.Optional[str],
            typing.Tuple[Reference],
            typing.Optional[str],
            typing.Union[None, str, int, float],
            str
        ]:
    """

    >>> parse_selector('pass', None)
    (None, 'pass', None, (), None, None, '')

    >>> parse_selector('prop[#test]!', None)
    (None, 'prop', None, (Reference(id='test', name=None, _source='#test'),), '!', None, '')

    >>> parse_selector('prop[#test]?', None)
    (None, 'prop', None, (Reference(id='test', name=None, _source='#test'),), '?', None, '')

    >>> parse_selector('prop[#test]?123', None)
    (None, 'prop', None, (Reference(id='test', name=None, _source='#test'),), '?', None, '123')

    >>> parse_selector('prop[#test]>0', None)
    (None, 'prop', None, (Reference(id='test', name=None, _source='#test'),), '>', 0, '')

    >>> parse_selector('prop[#test]>1_000', None)
    (None, 'prop', None, (Reference(id='test', name=None, _source='#test'),), '>', 1000, '')

    >>> parse_selector('prop[#test]>1.5', None)
    (None, 'prop', None, (Reference(id='test', name=None, _source='#test'),), '>', 1.5, '')

    >>> parse_selector('prop[#test]>-2', None)
    (None, 'prop', None, (Reference(id='test', name=None, _source='#test'),), '>', -2, '')

    >>> parse_selector('prop[#test]>-2e2', None)
    (None, 'prop', None, (Reference(id='test', name=None, _source='#test'),), '>', -200.0, '')

    >>> parse_selector('prop[#test]>2e-2', None)
    (None, 'prop', None, (Reference(id='test', name=None, _source='#test'),), '>', 0.02, '')

    >>> parse_selector('prop[#test]=="test string"', None)
    (None, 'prop', None, (Reference(id='test', name=None, _source='#test'),), '==', 'test string', '')

    >>> parse_selector('prop[#test]>0 123', None)
    (None, 'prop', None, (Reference(id='test', name=None, _source='#test'),), '>', 0, ' 123')

    >>> parse_selector('%mod prop[@recipe#test]=="test" => such wow', None)
    ('mod', 'prop', 'recipe', (Reference(id='test', name=None, _source='#test'),), '==', 'test', ' => such wow')

    :return:
    """
    mod, reference = parse_mod(selector)
    type_, provider, refs, remainder = parse_reference(reference, task_id)
    if not type_:
        # A selector without reference makes no sense
        raise ValueError(f"Invalid selector {selector!r}")

    m_oper_value = CONDITION_RE.match(remainder)

    if m_oper_value:
        oper = m_oper_value.group('oper')
        value = m_oper_value.group('value')
    else:
        oper, value = None, None

    if oper or value:
        remainder = remainder[m_oper_value.end(m_oper_value.lastindex):]

    if oper:
        assert oper in OPERATIONS.keys()
    else:
        oper = None

    if value == '' or value is None:
        if oper not in OPERATIONS_WITHOUT_VALUE:
            raise ValueError(f"Invalid selector {selector!r} (operator {oper!r} requires a value)")

        value = None

    elif oper not in OPERATIONS_WITHOUT_VALUE:
        if value.startswith("'"):
            assert value.endswith("'")
            value = value[1:-1]
        elif value.startswith('"'):
            assert value.endswith('"')
            value = value[1:-1]
        elif '.' in value or 'e' in value:
            value = float(value)
        else:
            value = int(value)

    elif value:
        # The operator does not expect a value, so it's part of the remainder
        remainder = value + remainder
        value = None

    return mod, type_, provider, refs, oper, value, remainder


def filter_by_selector(selector: str, bundles: Providers) \
        -> typing.Tuple[typing.Optional[str], typing.Tuple[Element], str]:

    """
    Resolve selector: returns the elements matching the query.
    """
    mod, type_, provider, refs, oper, value, remainder = parse_selector(selector, bundles.task_id)
    if mod:
        raise ValueError(f"Invalid modifier {mod!r} for selector {selector!r}")

    try:
        matches = match_reference(type_, provider, refs, bundles)
    except ValueError as exc:
        raise ValueError(f"Invalid {type_!r} selector {selector!r}: {exc}")

    attr = VALUE_ATTR.get(type_, VALUE_ATTR[None])
    oper = OPERATIONS.get(oper)

    results: typing.MutableSequence[Element] = collections.deque()
    for match in matches:
        obj_values = [getattr(mv, attr, None) for mv in match.values]
        for obj_value in obj_values:
            if oper(obj_value, value):
                results.append(match.element)
                break

    return provider, tuple(results), remainder


def match_by_selector(selector: str, bundles: Providers) -> typing.Tuple[bool, str]:

    mod, type_, provider, refs, oper, value, remainder = parse_selector(selector, bundles.task_id)
    if mod and mod not in {'any', 'all'}:
        raise ValueError(f"Invalid modifier {mod!r} for selector {selector!r}")

    try:
        matches = match_reference(type_, provider, refs, bundles)
    except ValueError as exc:
        raise ValueError(f"Invalid {type_!r} selector {selector!r}: {exc}")

    attr = VALUE_ATTR.get(type_, VALUE_ATTR[None])
    oper = OPERATIONS.get(oper)

    for match in matches:
        obj_values = [getattr(mv, attr, None) for mv in match.values]
        if not obj_values and mod != 'any':
            return False, remainder

        for obj_value in obj_values:
            if mod == 'any':
                if oper(obj_value, value):
                    return True, remainder
            else:
                if not oper(obj_value, value):
                    return False, remainder

    return mod != 'any', remainder
