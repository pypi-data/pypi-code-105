from collections import ChainMap
from collections.abc import Mapping, Sequence, Set, MutableMapping
from typing import Optional

from nv.utils.collections.structures import merge_mappings


__ALL__ = ['serialize', 'parse', 'ObjectDict', 'DictObject']


# TODO: Revise ObjectDict using parser module


BASIC_TYPES = (
    str,
    bytes,
    int,
    float,
    bool,
    type(None),
)


class ObjectDict(MutableMapping):
    """
    Implements dictionary access to object attributes (e.g. for config files).  It also rebuilds itself
    from dictionaries using the constructor from_dict. Nested dictionaries are implemented as ObjectDicts,
    allowing dotted access to nested dictionaries.
    """
    def __init__(self, _recursive=True, _defaults: Optional[Mapping] = None, **kwargs):
        self.apply_mapping(kwargs, recursive=_recursive, defaults=_defaults)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __delitem__(self, key):
        delattr(self, key)

    def __len__(self):
        return len(self.__dict__)

    def __iter__(self):
        return iter(self.__dict__)

    def __repr__(self):
        return dict.__repr__(self.__dict__)

    def __str__(self):
        return dict.__str__(self.__dict__)

    def apply_mapping(self, d: Mapping, recursive=True, defaults: Optional[Mapping] = None):
        for k, v in ChainMap(d, defaults or dict()).items():
            setattr(self, k, parse(v) if recursive else v)

    @classmethod
    def from_dict(cls, d: Mapping, recursive=True, defaults: Optional[Mapping] = None) -> 'ObjectDict':
        instance = cls.__new__(cls)
        instance.apply_mapping(d, recursive=recursive, defaults=defaults)
        return instance

    def as_dict(self, recursive=True) -> dict:
        return {k: serialize(v) for k, v in self.__dict__.items()} if recursive else self.__dict__

    def merge_into(self, merger: Mapping) -> Mapping:
        return merge_mappings(self, merger)

    def incorporate(self, merged: Mapping):
        self.__dict__ = merge_mappings(merged, self.__dict__)


def apply_base_type(b, fn):
    return b


def apply_mapping(m: Mapping, fn) -> dict:
    return {k: fn(v) for k, v in m.items()}


def apply_sequence(s: Sequence, fn) -> list:
    return [fn(v) for v in s]


def apply_set(s: Set, fn) -> set:
    return {fn(v) for v in s}


def apply_as_dict(o: ObjectDict, fn):
    return o.as_dict()


def apply_from_dict(o, fn):
    return ObjectDict.from_dict(o)



SERIALIZERS_MAP = (
    (ObjectDict, apply_as_dict),
    (BASIC_TYPES, apply_base_type),
    (Set, apply_set),
    (Sequence, apply_sequence),
    (Mapping, apply_mapping),
)


_RaiseError = object()


def apply(obj, fn, type_map, default=_RaiseError):
    try:
        return next((d for t, d in type_map if isinstance(obj, t)))(obj, fn)
    except StopIteration:
        if default is _RaiseError:
            raise TypeError(f'Unable to {fn.__name__} type: {type(obj)}')
        return default


def serialize(obj, type_map=SERIALIZERS_MAP, default=_RaiseError):
    return apply(obj, serialize, type_map, default=default)


PARSERS_MAP = (
    (BASIC_TYPES, apply_base_type),
    (Set, apply_set),
    (Sequence, apply_sequence),
    (Mapping, apply_from_dict),
)


def parse(obj, type_map=PARSERS_MAP, default=_RaiseError):
    return apply(obj, parse, type_map, default=default)


class DictObject(dict):
    """
    Simple implementation of a dictionary that exposes its keys as attributes of an object. This is a simple
    plain vanilla implementation that does not enforce valid attribute names.
    """
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("Missing attribute: {name}".format(name=name))

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("Missing attribute: {name}".format(name=name))
