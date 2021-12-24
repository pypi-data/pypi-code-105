import logging

from ..datagenerator import ColumnPgInfo, Constraints, Statistics, generator, logging
from .legacy import generator_utils

"""
Generator for Postgres Boolean-Types (byteas)
https://www.postgresql.org/docs/9.5/datatype-boolean.html
"""


@generator("boolean")
def boolean_generator(
    stats: Statistics, column_info: ColumnPgInfo, constraints: Constraints, rows_to_gen
):
    if constraints.is_unique:
        if column_info.is_nullable:
            logging.warning(
                f"Column '{column_info.column_name}' ignored because boolean_generator does not support UNIQUE constraint."
            )
            return None
        else:
            raise Exception(
                f"Column '{column_info.column_name}' can't be generated because boolean_generator does not support UNIQUE constraint and is also NOT NULL."
            )
    return [generator_utils.random_boolean(postgres=False) for _ in range(rows_to_gen)]
