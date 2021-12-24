import random

import numpy as np

from ..datagenerator import (
    ColumnPgInfo,
    Constraints,
    StatisticQuery,
    Statistics,
    generator,
)


@generator(
    None,
    comment_identifier="COPY",
    custom_queries=[
        StatisticQuery(
            name="src_data", query="SELECT {column_name} as val FROM {table_name}"
        )
    ],
)
def copy_generator(
    stats: Statistics, column_info: ColumnPgInfo, constraints: Constraints, rows_to_gen
):
    data = [d["val"] for d in stats.custom_stats.get("src_data", [])]
    if len(data) > rows_to_gen:
        data = data[:rows_to_gen]
    elif len(data) < rows_to_gen:
        if column_info.is_nullable:
            data.extend([None] * (rows_to_gen - len(data)))
        elif not constraints.is_unique:
            data.extend([random.choice(data) for _ in range(rows_to_gen - len(data))])
        else:
            raise Exception(
                f"can upscale copy values for {column_info.table_name}.{column_info.column_name}, is unique and not nullable"
            )

    np.random.shuffle(data)
    return data
