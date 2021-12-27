from collections import ChainMap
from collections.abc import Mapping, Sequence, Set
from functools import partial


__ALL__ = ['build_parser', 'build_parsers_map', 'build_strict_parser', 'build_safe_parser', 'clean_up']


class MessageObject:
    def __init__(self, content, callable=None):
        self.content = content
        self.callable = callable

    def __repr__(self):
        return f'{self.content} {super().__repr__()}'

    def __call__(self, *args, **kwargs):
        return self.callable(*args, **kwargs) if self.callable else None


def raise_if_unknown(obj, *args, **kwargs):
    raise TypeError(f"Unable to parse type {type(obj)}")


def do_nothing(obj, *args, **kwargs):
    return obj


RAISE_IF_UNKNOWN = MessageObject('RAISE_IF_UNKNOWN', raise_if_unknown)
DO_NOTHING = MessageObject('DO_NOTHING', do_nothing)
CLEAN_UP = MessageObject('CLEAN_UP')
NOT_FOUND = MessageObject('NOT_FOUND')


BASIC_TYPES = (
    int,
    float,
    complex,
    bool,
    type(None),
)


BASIC_SEQUENCES = (
    str,
    bytes,
    bytearray,
)


BASIC_ELEMENTS = (
    *BASIC_TYPES,
    *BASIC_SEQUENCES,
)


BASIC_STRUCTURES = (
    Set,
    Sequence,
    Mapping,
)


CLEANABLES = (
    *BASIC_SEQUENCES,
    *BASIC_STRUCTURES,
)


def _clean_up(result, clean_up):
    return result or CLEAN_UP if result in CLEANABLES and clean_up else result


def parse_element(obj, *args, element_parser=RAISE_IF_UNKNOWN, clean_up=False, **kwargs):
    return _clean_up(element_parser(obj, **kwargs), clean_up=clean_up)


def parse_set(obj: Set, parser, clean_up=False, **kwargs) -> set:
    return _clean_up(
        set(
            i for i in (
                parser(raw_i, clean_up=clean_up, **kwargs) for raw_i in obj
            ) if i is not CLEAN_UP),
        clean_up=clean_up,
    )


def parse_sequence(obj: Sequence, parser, clean_up=False, **kwargs) -> list:
    return _clean_up(
        list(
            i for i in (
                parser(raw_i, clean_up=clean_up, **kwargs) for raw_i in obj
            ) if i is not CLEAN_UP),
        clean_up=clean_up,
    )


def parse_mapping(obj: Mapping, parser, clean_up=False, parse_keys=False, **kwargs) -> dict:
    return _clean_up(
        dict(
            (k,v) for k, v in(
                (parser(raw_k, clean_up=clean_up, parse_keys=parse_keys, **kwargs) if parse_keys else raw_k,
                 parser(raw_v, clean_up=clean_up, parse_keys=parse_keys, **kwargs)) for raw_k, raw_v in obj.items()
        ) if k is not CLEAN_UP and v is not CLEAN_UP),
        clean_up=clean_up
    )


def parse_tuple(obj: tuple, parser, clean_up=False, **kwargs) -> tuple:
    return _clean_up(
        tuple(
            i for i in (
                parser(raw_i, clean_up=clean_up, **kwargs) for raw_i in obj
            ) if i is not CLEAN_UP),
        clean_up=clean_up,
    )


STRUCTURE_PARSERS = (
    (Set, parse_set),
    (Sequence, parse_sequence),
    (Mapping, parse_mapping),
)


DEFAULT_PARSERS = (
    (BASIC_ELEMENTS, parse_element),
    *STRUCTURE_PARSERS,
)


def build_parsers_map(element_parser, elements=BASIC_ELEMENTS, structure_parsers=STRUCTURE_PARSERS):
    return (
        (elements, element_parser),
        *structure_parsers,
    )


def build_parser(element_parser, parsers=DEFAULT_PARSERS, default_parser=None, **build_kwargs):
    default_parser = partial(parse_element, element_parser=default_parser or element_parser)
    build_clean_up = build_kwargs.setdefault('clean_up', None)
    build_parsers = build_kwargs.setdefault('parsers', parsers)

    def parser(obj, parsers=build_parsers, **parser_kwargs):
        parser_kwargs.setdefault('clean_up', build_clean_up)
        parser_kwargs.setdefault('element_parser', element_parser)
        parser_kwargs.setdefault('default_parser', default_parser)
        debug = parser_kwargs.setdefault('debug', False)

        call_kwargs = ChainMap(parser_kwargs, build_kwargs)

        def internal_parser(obj, **kwargs):
            selected_parser = next(
                (p for t, p in parsers if isinstance(obj, t)),
                default_parser
            )
            return selected_parser(obj, internal_parser, **kwargs)

        def debug_parser(obj, **kwargs):
            debug = kwargs.setdefault('debug', False)

            selected_parser = next(
                (p for t, p in parsers if isinstance(obj, t)),
                default_parser
            )

            if debug:
                print(f'internal_parser got:\n obj={obj!r}\n type={type(obj)}\n kwargs={kwargs}')
                print(f' internal_parser selected: {selected_parser.__name__} ({selected_parser!r})')

            result = selected_parser(obj, debug_parser, **kwargs)

            if debug:
                print(f' parsed result: {result!r}')

            return result

        result = internal_parser(obj, **call_kwargs) if not debug else debug_parser(obj, **call_kwargs)
        return result if result is not CLEAN_UP else None

    return parser


build_strict_parser = partial(build_parser, default_parser=RAISE_IF_UNKNOWN)

build_safe_parser = partial(build_parser, default_parser=DO_NOTHING)


def clean_up_structures(obj, *args, **kwargs):
    return (obj or CLEAN_UP) if isinstance(obj, BASIC_STRUCTURES) else obj


def clean_up_all(obj, *args, **kwargs):
    if isinstance(obj, CLEANABLES) or obj is None:
        return obj or CLEAN_UP
    return obj


clean_up = build_parser(clean_up_all, clean_up=True)
