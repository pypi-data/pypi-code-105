from collections import OrderedDict
from collections.abc import Mapping, Sequence, Set
from copy import copy
from itertools import chain
from typing import TypeVar, Union


__ALL__ = ['merge']


T = TypeVar('T')
V = TypeVar('V')


def _cast(result, original, fallback):
    cast = type(original)
    try:
        return cast(result)
    except TypeError:
        return fallback(result)


def merge_mappings(merged: Mapping, merger: Mapping) -> Mapping:
    merged = merged or dict()
    result = OrderedDict(merger)
    for k, v in merged.items():
        result[k] = merge(v, merger[k]) if k in merger else v
    return _cast(result, merger, dict)


def merge_sets(merged: Set, merger: Set) -> Set:
    merged = set(merged) if merged else set()
    return _cast(merged.union(set(merger)), merger, set)


def merge_sequences(merged: Set, merger: Set) -> Set:
    return _cast(chain(merged or list(), merger), merger, list)


def keep_merger_copy_if_not_none(merged, merger):
    return copy(merger) if merger is not None else copy(merged)


def keep_merger_copy_if_true(merged, merger):
    return copy(merger) if merger else copy(merged)


def keep_merger_if_not_none(merged, merger):
    return merger if merger is not None else merged


def raise_if_unknown(merger, merged):
    raise TypeError(f"Don't know how to merge {type(merger)} into {type(merged)}")


BASIC_TYPES = (
    int,
    float,
    bool,
    type(None),
)


BASIC_SEQUENCES = (
    str,
    bytes,
)


MERGERS_MAP_STRICT = (
    (BASIC_TYPES, keep_merger_copy_if_not_none),
    (BASIC_SEQUENCES, keep_merger_copy_if_true),
    (Mapping, merge_mappings),
    (Set, merge_sets),
    (Sequence, merge_sequences),
)


MERGERS_MAP = (
    *MERGERS_MAP_STRICT,
    # Catch all objects
    (object, keep_merger_if_not_none),
)


def merge(merged: T, merger: V, type_map=MERGERS_MAP_STRICT) -> Union[T, V]:
    """
    Merge nested mappings, sequences, sets. In case of conflicts (i.e. non-mergeable values under same key),
    resolve_conflicts is called (default keeps merger if not None, else merged).
    """
    merge_fn = next((m for t, m in type_map if isinstance(merger, t)), None)
    return merge_fn(merged, merger) if merge_fn is not None else raise_if_unknown(merged, merger)
