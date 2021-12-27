"""
    <type> "[" [ "@" <provider> ] [ "#" <id> [ "," <id> ]* ] [ ":" [ <ref> ] ] "]"

    * type: <outcome> or "prop"/"property", "file", "opt"/"option"
    * outcome: "pass", "fail", "error", "skip", "not-pass", "not-fail", "not-error", "not-skip"
    * ref depends on <type>
      * <outcome>: empty
      * "file": <class> "#" <name>
      * "prop": <name>
      * "opt": <name> "@" <domain>

    pass[@result#id]
    pass[#id]
    prop[@result#id1,id2:name]     @result is default and only provider, it's optional
    prop[#id1,id2:name]
    file[@config:class#name]
    file[@recipe#id:class#name]
    file[@step:class#name]
    opt[@config:domain#name]     domain is optional and defaults to "checklet"
    opt[@recipe#id:domain#name]
    opt[@step:domain#name]
    opt[@step:name]

"""
import collections
import typing
from dataclasses import dataclass

from momotor.bundles import ResultsBundle
from momotor.bundles.elements.base import Element
from momotor.bundles.elements.files import FilesMixin
from momotor.bundles.elements.options import OptionsMixin, Option
from momotor.bundles.elements.properties import PropertiesMixin
from momotor.bundles.elements.result import Outcome, Result
from momotor.bundles.utils.text import smart_split
from momotor.options.parser.consts import VALUE_ATTR, REFERENCE_RE, PROVIDER_RE, REF_RE
from momotor.options.parser.modifier import parse_mod, apply_combiner_modifier
from momotor.options.providers import Providers
from momotor.options.task_id import StepTaskId, apply_task_number


def _split_reference(reference: str) \
        -> typing.Tuple[typing.Optional[str], typing.Optional[str], str]:

    """

    >>> _split_reference("type")
    ('type', None, '')

    >>> _split_reference("type rest")
    ('type', None, ' rest')

    >>> _split_reference("type[]")
    ('type', '', '')

    >>> _split_reference("type []")
    ('type', '', '')

    >>> _split_reference("type[ ]")
    ('type', '', '')

    >>> _split_reference("type[] rest")
    ('type', '', ' rest')

    >>> _split_reference("type[option]")
    ('type', 'option', '')

    >>> _split_reference("type [option]")
    ('type', 'option', '')

    >>> _split_reference("type [ option ]")
    ('type', 'option', '')

    >>> _split_reference("type[option] ")
    ('type', 'option', ' ')

    :param reference:
    :return:
    """
    m_ref = REFERENCE_RE.match(reference)
    if m_ref is None:
        return None, None, reference

    type_ = m_ref.group('type')
    ref_option = m_ref.group('opt')
    if ref_option:
        ref_option = ref_option[1:-1].strip()

    remainder = reference[m_ref.end(m_ref.lastindex):]

    return type_, ref_option, remainder


@dataclass(frozen=True)
class Reference:
    id: typing.Optional[str]
    name: typing.Optional[str]

    _source: str


def _split_options(ref_option: str, task_id: typing.Optional[StepTaskId]) \
        -> typing.Tuple[typing.Optional[str], typing.Tuple[Reference], str]:

    """

    Not all of these variants make sense, but the syntax is legal

    >>> _split_options('@provider', None)
    ('provider', (), '')

    >>> _split_options('@provider#id', None)
    ('provider', (Reference(id='id', name=None, _source='#id'),), '')

    >>> _split_options('@provider:class#name', None)
    ('provider', (Reference(id=None, name='class#name', _source=':class#name'),), '')

    >>> _split_options('@provider:name', None)
    ('provider', (Reference(id=None, name='name', _source=':name'),), '')

    >>> _split_options('@provider#id:class#name', None)
    ('provider', (Reference(id='id', name='class#name', _source='#id:class#name'),), '')

    >>> _split_options('@provider#id:name', None)
    ('provider', (Reference(id='id', name='name', _source='#id:name'),), '')

    >>> _split_options('@provider #id, id2 : class#name', None)
    ('provider', (Reference(id='id', name='class#name', _source='#id, id2 : class#name'), Reference(id='id2', name='class#name', _source='#id, id2 : class#name')), '')

    >>> _split_options('#id', None)
    (None, (Reference(id='id', name=None, _source='#id'),), '')

    >>> _split_options('#id:name', None)
    (None, (Reference(id='id', name='name', _source='#id:name'),), '')

    >>> _split_options('#id:class#name', None)
    (None, (Reference(id='id', name='class#name', _source='#id:class#name'),), '')

    >>> _split_options(':name', None)
    (None, (Reference(id=None, name='name', _source=':name'),), '')

    >>> _split_options(':class#name', None)
    (None, (Reference(id=None, name='class#name', _source=':class#name'),), '')

    >>> _split_options('#id, id2', None)
    (None, (Reference(id='id', name=None, _source='#id, id2'), Reference(id='id2', name=None, _source='#id, id2')), '')

    >>> _split_options('#id.$0:class#name', StepTaskId('test', (11,)))
    (None, (Reference(id='id.11', name='class#name', _source='#id.$0:class#name'),), '')

    >>> _split_options('#id.$1:class#name', StepTaskId('test', (11, 12)))
    (None, (Reference(id='id.12', name='class#name', _source='#id.$1:class#name'),), '')

    >>> _split_options('#id.$@:class#name', StepTaskId('test', (11, 12)))
    (None, (Reference(id='id.11.12', name='class#name', _source='#id.$@:class#name'),), '')

    >>> _split_options('#id.$0-1:class#name', StepTaskId('test', (11, 12)))
    (None, (Reference(id='id.10', name='class#name', _source='#id.$0-1:class#name'),), '')

    >>> _split_options('#id.$1+1:class#name', StepTaskId('test', (11, 12)))
    (None, (Reference(id='id.13', name='class#name', _source='#id.$1+1:class#name'),), '')

    >>> _split_options('#id.$1/2:class#name', StepTaskId('test', (11, 12)))
    (None, (Reference(id='id.6', name='class#name', _source='#id.$1/2:class#name'),), '')

    >>> _split_options('#id.$1*2:class#name', StepTaskId('test', (11, 12)))
    (None, (Reference(id='id.24', name='class#name', _source='#id.$1*2:class#name'),), '')

    >>> _split_options('#id.$1%10:class#name', StepTaskId('test', (11, 12)))
    (None, (Reference(id='id.2', name='class#name', _source='#id.$1%10:class#name'),), '')

    :param ref_option:
    :return:
    """
    m_provider = PROVIDER_RE.match(ref_option)

    provider = m_provider.group('provider')
    if provider:
        remaining = ref_option[m_provider.end(m_provider.lastindex):]
    else:
        remaining = ref_option

    refs: typing.MutableSequence[Reference] = collections.deque()
    if remaining.strip():
        m_ref = REF_RE.match(remaining)
        if m_ref:
            ids_str = m_ref.group('ids')
            name = m_ref.group('name') or None
        else:
            ids_str, name = None, None

        if ids_str or name:
            end_pos = m_ref.end(m_ref.lastindex)
            source, remaining = remaining[:end_pos].strip(), remaining[end_pos:]

            ids: typing.List[typing.Optional[str]]
            if not ids_str:
                ids = [None]
            else:
                ids = [id_.strip() for id_ in ids_str.split(',')]

            for id_ in ids:
                if id_ or name:
                    if id_ and task_id:
                        id_ = apply_task_number(id_, task_id)

                    refs.append(
                        Reference(id_, name, source)
                    )

    return provider, tuple(refs), remaining


def parse_reference(reference: str, task_id: typing.Optional[StepTaskId]) \
        -> typing.Tuple[str, typing.Optional[str], typing.Tuple[Reference], str]:
    """

    >>> parse_reference("type", None)
    ('type', None, (), '')

    >>> parse_reference("type rest", None)
    ('type', None, (), ' rest')

    >>> parse_reference("type[] rest", None)
    ('type', None, (), ' rest')

    >>> parse_reference("type[@provider] rest", None)
    ('type', 'provider', (), ' rest')

    >>> parse_reference("type[@provider#id:class#name] rest", None)
    ('type', 'provider', (Reference(id='id', name='class#name', _source='#id:class#name'),), ' rest')

    >>> parse_reference("type[@provider#id,id2:class#name] rest", None)
    ('type', 'provider', (Reference(id='id', name='class#name', _source='#id,id2:class#name'), Reference(id='id2', name='class#name', _source='#id,id2:class#name')), ' rest')

    >>> parse_reference("type[@provider#id.$0,id2.$1:class#name] rest", StepTaskId('test', (11, 12,)))
    ('type', 'provider', (Reference(id='id.11', name='class#name', _source='#id.$0,id2.$1:class#name'), Reference(id='id2.12', name='class#name', _source='#id.$0,id2.$1:class#name')), ' rest')

    """
    type_, ref_option, remainder = _split_reference(reference)

    if ref_option:
        provider, refs, ref_remainder = _split_options(ref_option, task_id)
        if ref_remainder and ref_remainder.strip():
            raise ValueError(f"Invalid reference {reference.strip()}")

    else:
        provider, refs = None, tuple()

    return type_, provider, refs, remainder


def _resolve_id_references(objects: typing.Mapping, refs: typing.Sequence[Reference]) \
        -> typing.Generator[typing.Tuple[typing.Any, typing.Optional[Reference]], None, None]:

    if not refs:
        for obj in objects.values():
            yield obj, None

    for ref in refs:
        if ref.id:
            try:
                yield objects[ref.id], ref
            except KeyError:
                pass
        else:
            for result in objects.values():
                yield result, ref


def _duplicate_references(obj: typing.Any, refs: typing.Sequence[Reference]) \
        -> typing.Generator[typing.Tuple[typing.Any, typing.Optional[Reference]], None, None]:

    if not refs:
        yield obj, None

    for ref in refs:
        yield obj, ref


def _split_name_class(nc: str) -> typing.Tuple[str, typing.Optional[str]]:
    """

    >>> _split_name_class('name')
    ('name', None)

    >>> _split_name_class('class#name')
    ('name', 'class')

    >>> _split_name_class('class#"name"')
    ('"name"', 'class')

    >>> _split_name_class('class#*.txt')
    ('*.txt', 'class')

    >>> _split_name_class('class#"spaced name.txt"')
    ('"spaced name.txt"', 'class')

    >>> _split_name_class('class#"name"123' + "'test'")
    ('"name"123\\'test\\'', 'class')

    >>> _split_name_class('"noclass#name"')
    ('"noclass#name"', None)

    >>> _split_name_class('"spaced name.txt"')
    ('"spaced name.txt"', None)

    :param nc:
    :return:
    """
    parts = list(smart_split(nc))

    if parts and '#' in parts[0] and parts[0][0] not in {'"', "'"}:
        class_, rest = parts[0].split('#', 1)
        if rest:
            parts[0] = rest
        else:
            parts.pop(0)

    else:
        class_ = None

    return ''.join(parts), class_


def _split_name_domain(nd: str) -> typing.Tuple[str, typing.Optional[str]]:
    if '@' in nd:
        name, domain = nd.split('@', 1)
    else:
        name, domain = nd, None

    return name, domain


@dataclass(frozen=True)
class ReferenceMatch:
    element: Element
    values: typing.Tuple


def _match_outcome_reference(type_: str, objects: typing.Iterable[typing.Tuple[Result, Reference]]) \
        -> typing.Generator[ReferenceMatch, None, None]:

    if type_.startswith('not-'):
        try:
            outcome = Outcome(type_[4:])
        except ValueError:
            raise ValueError(f"Invalid type {type_}")

        _test = lambda obj: obj.outcome_enum != outcome

    else:
        try:
            outcome = Outcome(type_)
        except ValueError:
            raise ValueError(f"Invalid type {type_}")

        _test = lambda obj: obj.outcome_enum == outcome

    for obj, ref in objects:
        obj = typing.cast(Result, obj)

        if ref and ref.name:
            # noinspection PyProtectedMember
            raise ValueError(
                f"{ref._source!r} is not valid: name or class not allowed"
            )

        result = (obj,) if _test(obj) else tuple()
        yield ReferenceMatch(obj, result)


def _match_prop_reference(objects: typing.Iterable[typing.Tuple[typing.Union[Element, PropertiesMixin], Reference]]) \
        -> typing.Generator[ReferenceMatch, None, None]:

    for obj, ref in objects:
        if ref is None:
            raise ValueError("a name is required")
        elif ref.name is None:
            # noinspection PyProtectedMember
            raise ValueError(
                f"{ref._source!r} is not valid: a name is required"
            )

        properties = obj.properties.filter(name=ref.name)
        yield ReferenceMatch(obj, properties)


def _match_file_reference(objects: typing.Iterable[typing.Tuple[typing.Union[Element, FilesMixin], Reference]]) \
        -> typing.Generator[ReferenceMatch, None, None]:

    for obj, ref in objects:
        files = obj.files
        if ref and ref.name:
            name, class_ = _split_name_class(ref.name)

            filters = {}
            if name:
                filters['name__glob'] = name
            if class_:
                filters['class_'] = class_

            files = files.filter(**filters)

        yield ReferenceMatch(obj, files)


def _match_opt_reference(objects: typing.Iterable[typing.Tuple[typing.Union[Element, OptionsMixin], Reference]]) \
        -> typing.Generator[ReferenceMatch, None, None]:

    for obj, ref in objects:
        if ref is None:
            raise ValueError("a name is required")
        elif ref.name is None:
            # noinspection PyProtectedMember
            raise ValueError(
                f"{ref._source!r} is not valid: a name is required"
            )

        name, domain = _split_name_domain(ref.name)

        options = obj.options.filter(name=name, domain=domain or Option.DEFAULT_DOMAIN)
        yield ReferenceMatch(obj, options)


def _get_bundle_objects(provider, refs, bundles):
    if provider is None:
        raise ValueError(f"no provider")
    elif provider == 'recipe' and bundles.recipe:
        objects = _duplicate_references(bundles.recipe, refs)
    elif provider == 'config' and bundles.config:
        objects = _duplicate_references(bundles.config, refs)
    elif provider == 'product' and bundles.product:
        objects = _duplicate_references(bundles.product, refs)
    elif provider == 'step' and bundles.recipe and bundles.task_id:
        try:
            step = bundles.recipe.steps[bundles.task_id.step_id]
        except KeyError:
            raise ValueError(f"invalid provider {provider!r} for task {bundles.task_id!s}")

        objects = _duplicate_references(step, refs)
    elif provider == 'result' and bundles.results:
        objects = _resolve_id_references(bundles.results.results, refs)
    else:
        raise ValueError(f"invalid provider {provider!r}")

    return objects


def match_reference(
    type_: str, provider: typing.Optional[str], refs: typing.Tuple[Reference], bundles
) -> typing.Generator[ReferenceMatch, None, None]:
    if type_ in {'opt', 'file'}:
        objects = _get_bundle_objects(provider, refs, bundles)

    else:
        if (provider and provider != 'result') or not bundles.results:
            raise ValueError(f"invalid provider {provider!r}")

        objects = _resolve_id_references(bundles.results.results, refs)

    if type_ == 'prop':
        yield from _match_prop_reference(objects)

    elif type_ == 'file':
        yield from _match_file_reference(objects)

    elif type_ == 'opt':
        yield from _match_opt_reference(objects)

    else:
        yield from _match_outcome_reference(type_, objects)


def select_by_reference(reference: str, bundles: Providers) \
        -> typing.Tuple[typing.Optional[str], typing.Tuple[ReferenceMatch], str]:

    """ Parse a reference string and collect the referenced items
    """

    type_, provider, refs, remainder = parse_reference(reference, bundles.task_id)
    try:
        if type_:
            items = tuple(match_reference(type_, provider, refs, bundles))
        else:
            items = tuple()

    except ValueError as exc:
        raise ValueError(f"Invalid {type_!r} reference {reference!r}: {exc}")

    return type_, items, remainder


def select_by_prop_reference(reference: str, results: ResultsBundle = None, task_id: StepTaskId = None) \
        -> typing.Tuple[typing.Tuple[ReferenceMatch], str]:

    provider, refs, remainder = _split_options(reference, task_id)

    try:
        if (provider and provider != 'result') or not results:
            raise ValueError(f"invalid provider {provider!r}")

        objects = _resolve_id_references(results.results, refs)
    except ValueError as exc:
        raise ValueError(f"Invalid property reference {reference!r}: {exc}")

    return tuple(_match_prop_reference(objects)), remainder


def select_by_file_reference(reference: str, bundles: Providers) -> typing.Tuple[typing.Tuple[ReferenceMatch], str]:
    provider, refs, remainder = _split_options(reference, bundles.task_id)

    try:
        objects = _get_bundle_objects(provider, refs, bundles)
    except ValueError as exc:
        raise ValueError(f"Invalid file reference {reference!r}: {exc}")

    return tuple(_match_file_reference(objects)), remainder


def select_by_opt_reference(reference: str, bundles: Providers) -> typing.Tuple[typing.Tuple[ReferenceMatch], str]:
    provider, refs, remainder = _split_options(reference, bundles.task_id)

    try:
        objects = _get_bundle_objects(provider, refs, bundles)
    except ValueError as exc:
        raise ValueError(f"Invalid option reference {reference!r}: {exc}")

    return tuple(_match_opt_reference(objects)), remainder


def resolve_value_reference(reference: str, bundles: Providers) \
        -> typing.Tuple[typing.Union[str, int, float, bool, None], str]:

    mod, remaining = parse_mod(reference)
    type_, provider, refs, remaining = parse_reference(remaining, bundles.task_id)

    if not type_:
        return None, reference

    matches = tuple(
        match_reference(type_, provider, refs, bundles)
    )

    attr = VALUE_ATTR.get(type_, VALUE_ATTR[None])

    values = collections.deque()
    for match in matches:
        if match.values:
            values.extend(getattr(value, attr, None) for value in match.values)
        else:
            values.append(None)

    return apply_combiner_modifier(mod or 'join', values), remaining
