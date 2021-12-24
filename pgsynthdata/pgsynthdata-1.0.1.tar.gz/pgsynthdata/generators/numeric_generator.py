import logging

from ..datagenerator import (
    ColumnPgInfo,
    Constraints,
    StatisticQuery,
    Statistics,
    generator,
)
from . import generator_utils
from .legacy import generator_utils as legacy_utils
from .legacy import numeric_generator as legacy_numeric_generator

"""
Generator for Postgres Nummeric-Types (excluding serial-types)
https://www.postgresql.org/docs/9.5/datatype-numeric.html
Important: Despite the website, there is no 'decimal' type in postgres. It is same as 'numeric'
"""

QUERIES = [
    StatisticQuery(
        name="absolut_min", query="SELECT MIN({column_name}) FROM {table_name}"
    ),
    StatisticQuery(
        name="absolut_max", query="SELECT MAX({column_name}) FROM {table_name}"
    ),
]


@generator(
    {"integer", "smallint", "bigint", "numeric", "double precision", "real"},
    custom_queries=QUERIES,
)
def numeric_generator(
    stats: Statistics, column_info: ColumnPgInfo, constraints: Constraints, rows_to_gen
):
    # HINT everything below is a wrapper for the legacy generator

    min_bound, max_bound = None, None
    if column_info.data_type in {"integer", "smallint", "bigint"}:
        min_bound, max_bound, _ = generator_utils.determine_boundaries_int(stats)
    else:
        min_bound, max_bound, _ = generator_utils.determine_boundaries_float(stats)

    if constraints.is_unique:
        return legacy_numeric_generator.get_numeric_vals_primary_constraint(
            column_info.data_type,
            rows_to_gen,
            min_bound,
            max_bound,
            stats.pg_stats.histogram_bounds,
        )

    if constraints.fk_values:
        raise Exception("For FK's the fk_generator should be used!")

    number_of_row_BEFORE_MF = rows_to_gen  # HINT wont' work with Multiplication-Factor

    generated_freqs, distinct_values = legacy_utils.determine_frequency(
        number_of_row_BEFORE_MF,
        rows_to_gen,
        stats.pg_stats.most_common_vals,
        stats.pg_stats.most_common_freqs,
        stats.pg_stats.n_distinct,
    )

    generated_values = legacy_numeric_generator.get_numeric_vals_no_constraints(
        column_info.data_type,
        distinct_values,
        min_bound,
        max_bound,
        column_info.numeric_precision,
        column_info.numeric_precision_radix,
        column_info.numeric_scale,
        stats.pg_stats.histogram_bounds,
    )

    generated_values = legacy_utils.select_generator_mode(
        generated_values, generated_freqs, stats.pg_stats.null_frac, rows_to_gen
    )

    # HINT: Fallback
    if not generated_values:
        logging.warning(f"{__name__}: no generated_values, using fallback generator")
        generated_values = []
        for _ in range(rows_to_gen):
            generated_values.append(
                legacy_utils.random_number(
                    column_info.numeric_precision,
                    column_info.numeric_precision_radix,
                    column_info.numeric_scale,
                )
            )

    return generated_values
