import logging

from ..datagenerator import ColumnPgInfo, Constraints, Statistics, generator
from .legacy import generator_utils as legacy_utils
from .legacy import varchar_generator as legacy_varchar_generator

"""
Generator for Postgres Character-Types (varchar, text,...)
https://www.postgresql.org/docs/9.5/datatype-character.html
"""


@generator({"text", "character varying", "character"})
def character_generator(
    stats: Statistics, column_info: ColumnPgInfo, constraints: Constraints, rows_to_gen
):

    # HINT everything below is a wrapper for the legacy generator

    list_for_bounds = (
        stats.pg_stats.most_common_elems or stats.pg_stats.histogram_bounds
    )

    if constraints.used_as_fk_by or constraints.is_unique:
        return legacy_varchar_generator.get_varchar_primary_constraints(
            rows_to_gen,
            stats.pg_stats.avg_width,
            list_for_bounds,
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

    generated_values = legacy_varchar_generator.get_varchar_no_constraints(
        distinct_values,
        stats.pg_stats.avg_width,
        list_for_bounds,
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
                legacy_utils.random_word(
                    int(
                        column_info.character_maximum_length / 2.5
                    )  # HINT magic-number from legacy code. no transparent cause
                )
            )

    return generated_values
