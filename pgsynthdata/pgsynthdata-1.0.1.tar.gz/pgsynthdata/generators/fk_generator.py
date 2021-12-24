from ..datagenerator import (
    FK_GENERATOR_NAME,
    ColumnPgInfo,
    Constraints,
    Statistics,
    generator,
)
from .legacy import date_generator, numeric_generator, varchar_generator


def _minmax(fk_values):
    return min(fk_values), max(fk_values)


@generator(FK_GENERATOR_NAME)
def fk_generator(
    stats: Statistics, col_info: ColumnPgInfo, constraints: Constraints, rows_to_gen
):

    # HINT input data as needed for legacy generator
    ref_table, ref_column = "t", "c"
    pk_values = {
        ref_table: {ref_column: constraints.fk_values},
    }

    if col_info.data_type in {
        "integer",
        "smallint",
        "bigint",
        "numeric",
        "double precision",
        "real",
    }:
        min_bound, max_bound = _minmax(constraints.fk_values)
        return numeric_generator.get_numeric_vals_foreign_constraint(
            col_info.data_type,
            rows_to_gen,
            pk_values,
            ref_table,
            ref_column,
            min_bound,
            max_bound,
            stats.pg_stats.histogram_bounds,
        )
    elif col_info.data_type in {"date", "timestamp", "timestamp without time zone"}:
        min_bound, max_bound = _minmax(constraints.fk_values)
        return date_generator.get_data_foreign_constraint(
            rows_to_gen,
            pk_values,
            ref_table,
            ref_column,
            min_bound,
            max_bound,
        )
    elif col_info.data_type in {"text", "character varying", "character"}:
        return varchar_generator.get_varchar_foreign_constraint(
            rows_to_gen,
            pk_values,
            ref_table,
            ref_column,
        )
    else:
        raise Exception(f"FK-generator: type {col_info.data_type} is not supported")
