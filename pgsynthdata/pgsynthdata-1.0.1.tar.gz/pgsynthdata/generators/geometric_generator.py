import logging

from ..datagenerator import AsIs, ColumnPgInfo, Constraints, Statistics, generator
from .generator_utils import determine_boundaries_geometry
from .legacy import generator_utils as legacy_utils
from .legacy import geometry_generator as legacy_geometry_generator

"""
Generator for Postgres Geometric-Types
https://www.postgresql.org/docs/9.5/datatype-geometric.html
"""


@generator({"point", "line", "polygon", "circle", "box", "lseg", "path"})
def geometric_generator(
    stats: Statistics, column_info: ColumnPgInfo, constraints: Constraints, rows_to_gen
):

    # HINT everything below is a wrapper for the legacy generator

    _, max_bound, _ = determine_boundaries_geometry(stats)

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

    generated_values = legacy_geometry_generator.get_geometry_no_constraints(
        column_info.data_type, distinct_values, max_bound
    )

    generated_values = legacy_utils.select_generator_mode(
        generated_values, generated_freqs, stats.pg_stats.null_frac, rows_to_gen
    )

    # HINT: Fallback
    if not generated_values:
        logging.warning(f"{__name__}: No generated_values, using fallback generator")
        generated_values = ["NULL"] * rows_to_gen

    return list(map(AsIs, generated_values))
