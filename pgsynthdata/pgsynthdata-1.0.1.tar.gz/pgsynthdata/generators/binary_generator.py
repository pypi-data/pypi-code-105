import logging

from ..datagenerator import ColumnPgInfo, Constraints, Statistics, generator
from .legacy import bytea_generator as legacy_bytea_generator
from .legacy import generator_utils as legacy_utils

"""
Generator for Postgres Binary-Types (byteas)
https://www.postgresql.org/docs/9.5/datatype-binary.html
"""


@generator("bytea")
def binary_generator(
    stats: Statistics, column_info: ColumnPgInfo, constraints: Constraints, rows_to_gen
):

    # HINT everything below is a wrapper for the legacy generator

    if constraints.used_as_fk_by or constraints.is_unique:
        raise Exception("binary_generator: Does not support PK and UNIQUE types")

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

    generated_values = legacy_bytea_generator.get_bytea_no_constraints(distinct_values)

    generated_values = legacy_utils.select_generator_mode(
        generated_values, generated_freqs, stats.pg_stats.null_frac, rows_to_gen
    )

    # HINT: Fallback
    if not generated_values:
        logging.warning(f"{__name__}: No generated_values, using fallback generator")
        generated_values = ["NULL"] * rows_to_gen

    return generated_values
