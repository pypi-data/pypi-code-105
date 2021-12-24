import datetime
import logging

from ..datagenerator import ColumnPgInfo, Constraints, Statistics, generator
from .generator_utils import determine_boundaries_date, determine_boundaries_timestamp
from .legacy import date_generator as legacy_date_generator
from .legacy import generator_utils as legacy_utils

"""
Generator for Postgres Character-Types (varchar, text,...)
https://www.postgresql.org/docs/9.5/datatype-datetime.html
"""


@generator({"date", "timestamp without time zone"})
def datetime_generator(
    stats: Statistics, column_info: ColumnPgInfo, constraints: Constraints, rows_to_gen
):

    # HINT everything below is a wrapper for the legacy generator
    if column_info.data_type == "date":
        min_bound, max_bound, _ = determine_boundaries_date(stats)
    if column_info.data_type == "timestamp without time zone":
        min_bound, max_bound, _ = determine_boundaries_timestamp(stats)

    if constraints.used_as_fk_by or constraints.is_unique:
        return legacy_date_generator.get_date_primary_constraints(
            column_info.data_type, rows_to_gen, min_bound, max_bound
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

    generated_values = legacy_date_generator.get_data_no_constraints(
        column_info.data_type, distinct_values, min_bound, max_bound
    )

    generated_values = legacy_utils.select_generator_mode(
        generated_values, generated_freqs, stats.pg_stats.null_frac, rows_to_gen
    )

    # HINT: Fallback
    if not generated_values:
        logging.warning(f"{__name__}: no generated_values, using fallback generator")
        generated_values = []
        for _ in range(rows_to_gen):
            START_DATE = datetime.date(year=1950, month=1, day=1)
            END_DATE = datetime.date.today()
            generated_values.append(legacy_utils.random_date(START_DATE, END_DATE))

    return generated_values
