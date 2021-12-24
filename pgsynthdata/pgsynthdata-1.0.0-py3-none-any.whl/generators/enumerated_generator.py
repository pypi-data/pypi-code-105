import logging
import random

from ..datagenerator import (
    ColumnPgInfo,
    Constraints,
    StatisticQuery,
    Statistics,
    generator,
)


@generator(
    "USER-DEFINED",
    custom_queries=[
        StatisticQuery(
            name="enum_values",
            query="""
                  SELECT 
                    enu.enumlabel as label
                  FROM 
                    information_schema.columns col 
                    INNER JOIN pg_type typ ON col.udt_name = typ.typname 
                    INNER JOIN pg_enum enu ON typ.oid = enu.enumtypid 
                  WHERE 
                    col.table_name = {table_name_str}
                    AND col.column_name = {column_name_str}
                  """,
        ),
    ],
)
def enumerated_generator(
    stats: Statistics, column_info: ColumnPgInfo, constraints: Constraints, rows_to_gen
):
    if len(stats.custom_stats.get("enum_values", [])) > 0:
        return _enum_generator(stats, column_info, constraints, rows_to_gen)

    logging.warning(
        f"no USER-DEFINED-TYPE Generator for {column_info.table_name}.{column_info.column_name} with udt-name {column_info.udt_name}"
    )
    return None


def _enum_generator(
    stats: Statistics,
    column_info: ColumnPgInfo,
    constraints: Constraints,
    rows_to_gen,
):
    if constraints.is_unique:
        if column_info.is_nullable:
            logging.warning(
                f"Column '{column_info.column_name}' ignored because _enum_generator does not support UNIQUE constraint."
            )
            return None
        else:
            raise Exception(
                f"Column '{column_info.column_name}' can't be generated because _enum_generator does not support UNIQUE constraint and is also NOT NULL."
            )
    enum_values = stats.custom_stats.get("enum_values")
    enum_values = [r["label"] for r in enum_values] if enum_values else [None]
    return [random.choice(enum_values) for _ in range(rows_to_gen)]
