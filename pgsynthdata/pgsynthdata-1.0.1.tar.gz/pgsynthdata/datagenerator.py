import dataclasses
import logging
import os
import re
from dataclasses import dataclass
from importlib import import_module
from pathlib import Path
from typing import (
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    Union,
    no_type_check,
)

from psycopg2.extensions import (  # HINT can be imported by generators for user defined types
    AsIs,
)
from psycopg2.extras import DictRow

from .database import ColumnPgInfo, ColumnPgStats, empty_column_pg_stats


@dataclass
class StatisticQuery:
    name: str = ""
    query: str = ""


@dataclass
class Generator:
    function: Callable
    custom_queries: Optional[List[StatisticQuery]]


@dataclass
class Constraints:
    used_as_fk_by: List[Tuple[str, str]]
    is_unique: bool = False
    is_fk: bool = False
    fk_values: Optional[Iterable] = None


@dataclass
class Statistics:
    pg_stats: ColumnPgStats
    std_stats: Dict[str, List[DictRow]]
    custom_stats: Dict[str, List[DictRow]]


GENERATORS_FOLDER = "generators"
GENERATORS_SUFIX = "_generator.py"
MODULE_PREFIX = ".generators."
CURRENT_PACKAGE = "pgsynthdata"

_generators_tree: Dict[
    Union[str, None], Dict[Union[str, None], Dict[Union[str, None], Generator]]
] = {}
FK_GENERATOR_NAME = "_fk_generator"


def _import_generators():
    logging.info("start load generator plugins")

    path = Path(__file__).parent.joinpath(GENERATORS_FOLDER)
    for filename in os.listdir(path):
        if filename.endswith(GENERATORS_SUFIX):
            try:
                importname = MODULE_PREFIX + filename[:-3]
                import_module(importname, package=CURRENT_PACKAGE)
                logging.debug(f"successfully imported generator(s) '{filename}'")
            except ImportError as ex:
                logging.error(
                    f"ImportError while importing generator '{filename}:' {ex}"
                )
            except Exception as ex:
                logging.error(
                    f"Unknown Exception while importing generator '{filename}: {ex}'"
                )
                raise ex

    logging.info("finsih loading generator plugins")


# Generator registration decorator
def generator(
    data_types: Optional[Union[str, Set[str]]],
    udt_names_only: Union[str, Set[str]] = None,
    custom_queries: List[StatisticQuery] = None,
    comment_identifier: str = None,
):
    def decorator(func):
        gen = Generator(
            func,
            custom_queries,
        )
        for data_type in data_types if isinstance(data_types, set) else {data_types}:
            for udt_name in (
                udt_names_only if isinstance(udt_names_only, set) else {udt_names_only}
            ):
                _register(data_type, udt_name, comment_identifier, gen)
        return func

    return decorator


def _register(
    data_type: str, udt_name: str, comment_identifier: str, generator: Generator
):
    data_type = data_type.lower() if isinstance(data_type, str) else None
    udt_name = udt_name.lower() if isinstance(udt_name, str) else None
    comment_identifier = (
        comment_identifier.lower() if isinstance(comment_identifier, str) else None
    )
    if not comment_identifier in _generators_tree:
        _generators_tree[comment_identifier] = {}
    if not data_type in _generators_tree[comment_identifier]:
        _generators_tree[comment_identifier][data_type] = {}

    if udt_name in _generators_tree[comment_identifier][data_type]:
        logging.warning(
            f"generator for comment_identifier '{comment_identifier}' / data_type '{data_type}' / udt_name '{udt_name}'  is already registered (old={_generators_tree[comment_identifier][data_type][udt_name].function.__name__} / new={generator.function.__name__}"
        )
    _generators_tree[comment_identifier][data_type][udt_name] = generator
    logging.info(f"successfully registered generator '{generator.function.__name__}'")


def _get_from_generators_tree(
    keys: List[Union[str, None]],
    tree: Union[Dict, Generator, None] = _generators_tree,
) -> Union[Generator, None]:
    # if tree is no dict, it is either None or a Generator
    if not isinstance(tree, dict):
        return tree

    key = keys[0]
    gen = _get_from_generators_tree(keys[1:], tree.get(key, None))

    # fallback to less specific key (= bracktrace)
    if gen is None and key is not None:
        gen = _get_from_generators_tree(keys[1:], tree.get(None, None))

    return gen


def get_generator(
    pg_info: ColumnPgInfo, constraints: Constraints, pg_comment: str = None
) -> Optional[Generator]:
    udt_name = pg_info.udt_name.lower() if pg_info.udt_name else None
    datatype = pg_info.data_type.lower() if pg_info.data_type else None
    gen: Optional[Generator] = None
    if constraints.is_fk:
        gen = _get_from_generators_tree([None, FK_GENERATOR_NAME, None])
        if not gen or not isinstance(gen, Generator):
            raise KeyError("No FK-Generator found")
        return gen

    comment_identifier = _parse_comment(pg_comment)
    comment_identifier = (
        comment_identifier.lower() if isinstance(comment_identifier, str) else None
    )

    gen = _get_from_generators_tree([comment_identifier, datatype, udt_name])

    return gen


@no_type_check
def empty_statistics() -> Statistics:
    nones = [None for _ in dataclasses.fields(Statistics)]
    empty_stats = Statistics(*nones)
    empty_stats.pg_stats = empty_column_pg_stats()
    empty_stats.std_stats = {}
    empty_stats.custom_stats = {}
    return empty_stats


@no_type_check
def empty_contraints() -> Constraints:
    nones = [None for _ in dataclasses.fields(Constraints)]
    return Constraints(*nones)


def _parse_comment(comment: Optional[str]) -> Optional[str]:
    if not comment:
        return None

    prefix = "PGSYNTHDATA"
    pattern = re.compile(prefix + r"\[[a-zA-Z_\-]+\]")
    match = pattern.search(comment)
    if not match:
        return None
    return match.group()[len(prefix) + 1 : -1]


# HINT import plugins when this module is loaded
_import_generators()
