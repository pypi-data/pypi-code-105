import numpy as np

from ..datagenerator import (
    AsIs,
    ColumnPgInfo,
    Constraints,
    StatisticQuery,
    Statistics,
    generator,
)

"""
Generator for Postgres PostGIS spatial Types
https://postgis.net/docs/reference.html#Geometry_Accessors
supported: Points
"""


@generator(
    "USER-DEFINED",
    udt_names_only={"geometry"},
    custom_queries=[
        StatisticQuery(
            name="geometry_types",
            query="SELECT distinct GeometryType({column_name}) FROM {table_name}",
        ),
        StatisticQuery(
            name="point_minmax_xy",
            query="""
                select min(ST_X({column_name})) as min_x, max(ST_X({column_name})) as max_x, min(ST_Y({column_name})) as min_y, max(ST_Y({column_name})) as max_y
                FROM {table_name}
                WHERE GeometryType({column_name}) = 'POINT'
                """,
        ),
    ],
)
def spatial_generator(
    stats: Statistics, column_info: ColumnPgInfo, constraints: Constraints, rows_to_gen
):
    geometry_types = stats.custom_stats.get("geometry_types", [])
    if len(geometry_types) == 1 and geometry_types[0][0] == "POINT":
        min_x, max_x, min_y, max_y = stats.custom_stats["point_minmax_xy"][0]
        rand_x = np.random.uniform(low=min_x, high=max_x, size=rows_to_gen)
        rand_y = np.random.uniform(low=min_y, high=max_y, size=rows_to_gen)
        return [AsIs(f"ST_POINT({x},{y})") for (x, y) in zip(rand_x, rand_y)]

    return None  # HINT Geometry type not supported
