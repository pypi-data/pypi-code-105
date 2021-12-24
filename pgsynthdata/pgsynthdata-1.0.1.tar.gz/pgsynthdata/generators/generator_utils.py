from datetime import date, datetime
from typing import Any, Callable

from ..datagenerator import Statistics


def determine_boundaries(stats: Statistics, datatype_converter: Callable[[Any], Any]):

    min_value = None
    max_value = None
    list_for_bound = stats.pg_stats.most_common_vals or stats.pg_stats.histogram_bounds

    if list_for_bound:
        converted = [datatype_converter(e) for e in list_for_bound]
        min_value = min(converted)
        max_value = max(converted)

    return (
        min_value,
        max_value,
        list_for_bound,
    )


def determine_boundaries_float(stats: Statistics):
    return determine_boundaries(stats, float)


def determine_boundaries_int(stats: Statistics):
    min_bound, max_bound, boundaries = determine_boundaries(stats, int)
    if not min_bound or not max_bound:
        min_bound = stats.custom_stats["absolut_min"][0][0]
        max_bound = stats.custom_stats["absolut_max"][0][0]
    return min_bound, max_bound, boundaries


def determine_boundaries_string(stats: Statistics):
    return determine_boundaries(stats, len)


def determine_boundaries_date(stats: Statistics):
    if stats.pg_stats.most_common_vals or stats.pg_stats.histogram_bounds:
        return determine_boundaries(stats, lambda s: datetime.strptime(s, "%Y-%m-%d"))
    else:
        START_DATE = date(year=1950, month=1, day=1)
        END_DATE = date.today()
        return START_DATE, END_DATE, None


def determine_boundaries_timestamp(stats: Statistics):
    if stats.pg_stats.most_common_vals or stats.pg_stats.histogram_bounds:
        return determine_boundaries(
            stats, lambda s: datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
        )
    else:
        START_DATE = date(year=1950, month=1, day=1)
        END_DATE = date.today()
        return START_DATE, END_DATE, None


def determine_boundaries_geometry(stats: Statistics):
    min_value = max_value = 1000
    return min_value, max_value, None


def determine_boundaries_bytea(stats: Statistics):
    min_value = max_value = 8
    return min_value, max_value, None
