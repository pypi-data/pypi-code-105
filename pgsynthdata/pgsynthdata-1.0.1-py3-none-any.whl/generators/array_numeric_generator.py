import numpy as np

from pgsynthdata.database import simple_column_pg_infos
from pgsynthdata.generators.numeric_generator import numeric_generator

from ..datagenerator import (
    ColumnPgInfo,
    Constraints,
    StatisticQuery,
    Statistics,
    empty_contraints,
    empty_statistics,
    generator,
)
from .array_generator_utils import elements_to_arrays, generate_array_lengths

"""
Generator for Postgres Array-Types
https://www.postgresql.org/docs/9.5/arrays.html
"""

UDTNAME_TO_DATATYPE = {
    "_int2": "smallint",
    "_int4": "integer",
    "_int8": "bigint",
    "_numeric": "numeric",
    "_float8": "double precision",
}


@generator(
    "ARRAY",
    udt_names_only=set(UDTNAME_TO_DATATYPE.keys()),
    custom_queries=[
        StatisticQuery(
            "elem_stats",
            """select 
                min((select min(v) from unnest({column_name}) as t(v))),
                max((select max(v) from unnest({column_name}) as t(v))),
                (1-sum((select count(v) from unnest({column_name}) as t(v))) / sum((select count(*) from unnest({column_name}) as t(v)))) as null_frac
               from {table_name}""",
        )
    ],
)
def array_numeric_generator(
    stats: Statistics,
    column_info: ColumnPgInfo,
    constraints: Constraints,
    rows_to_gen: int,
):

    # 1: List mit den zu generierenden Längen erstellen (elem count histogramm)
    not_null_rows_to_gen = rows_to_gen
    null_rows_to_gen = 0
    if stats.pg_stats.null_frac != 0:
        not_null_rows_to_gen -= int(rows_to_gen * stats.pg_stats.null_frac)
        null_rows_to_gen = rows_to_gen - not_null_rows_to_gen

    to_generate_length = generate_array_lengths(stats, not_null_rows_to_gen)

    elements_to_gen = int(np.sum(to_generate_length))

    # 2: generate list with elements (use most_common_elems, and their freq)
    elem_stats = empty_statistics()

    elem_stats.custom_stats["absolut_min"] = [
        [stats.custom_stats["elem_stats"][0]["min"]]
    ]
    elem_stats.custom_stats["absolut_max"] = [
        [stats.custom_stats["elem_stats"][0]["max"]]
    ]
    elem_stats.pg_stats.n_distinct = 0.0

    if stats.pg_stats.most_common_elems and stats.pg_stats.most_common_freqs:
        elem_stats.pg_stats.most_common_vals = stats.pg_stats.most_common_elems
        freqs = stats.pg_stats.most_common_elem_freqs[
            : len(stats.pg_stats.most_common_elems)
        ]
        freqs = (freqs / np.sum(freqs)).tolist()  # HINT normalize so that sum=1.0
        elem_stats.pg_stats.most_common_freqs = freqs
        elem_stats.pg_stats.n_distinct = len(elem_stats.pg_stats.most_common_vals)

    # HINT Two or three additional values ... optionally the frequency of arrays with null elements (https://www.postgresql.org/docs/9.5/view-pg-stats.html)
    if (
        stats.pg_stats.most_common_elem_freqs
        and len(stats.pg_stats.most_common_elem_freqs)
        - len(stats.pg_stats.most_common_elems)
        == 3
        and stats.pg_stats.most_common_elem_freqs[-1] > 0.0
    ):
        elem_stats.pg_stats.null_frac = stats.custom_stats["elem_stats"][0]["null_frac"]
    else:
        elem_stats.pg_stats.null_frac = 0.0

    elem_column_info = simple_column_pg_infos(UDTNAME_TO_DATATYPE[column_info.udt_name])
    elem_column_info.numeric_precision = (
        64  # HINT doesnt matter as max_value is set, but needed by legacy generator
    )
    elem_column_info.numeric_precision_radix = 2
    elem_column_info.numeric_scale = (
        3 if column_info.udt_name in ["_numeric", "_float8"] else 0
    )
    elem_column_info.column_name = column_info.column_name

    elements = numeric_generator(
        stats=elem_stats,
        column_info=elem_column_info,
        constraints=empty_contraints(),
        rows_to_gen=elements_to_gen,
    )

    result_arrays = elements_to_arrays(to_generate_length, elements)
    if null_rows_to_gen > 0:
        result_arrays.extend([None] * null_rows_to_gen)
        np.random.shuffle(result_arrays)

    return result_arrays
