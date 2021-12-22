from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from time import time


class IntervalUnit(str, Enum):
    Y = "Y"
    M = "M"
    D = "D"
    H = "H"
    MIN = "min"
    S = "S"
    MS = "ms"


@dataclass
class Interval:
    value: int
    unit: IntervalUnit


def infer_format(datetime: str) -> str:
    # should follow the iso 8601 standard
    ...


def infer_freq():
    ...


DAYS_IN_MONTH = 28
DAYS_IN_YEAR = 365


def is_leap_year(v: int):
    return v % 4 or not v % 100 and v % 400


def infer_month(min: datetime, max: datetime, days: int):
    ...


def infer_interval_in_days(days: int):
    # TODO: should we take leap year into consideration?
    if days < DAYS_IN_MONTH:
        return Interval(days, IntervalUnit.D)

    if days < DAYS_IN_YEAR:
        return Interval(round(days / DAYS_IN_MONTH, 2), IntervalUnit.M)

    return Interval(round(days / DAYS_IN_YEAR, 2), IntervalUnit.Y)


SECONDS_IN_MINUTE = 60
SECONDS_IN_HOUR = 3600


def infer_interval_in_seconds(v: int):
    if v < SECONDS_IN_MINUTE:
        return Interval(v, IntervalUnit.S)

    if v < SECONDS_IN_HOUR:
        return Interval(round(v / SECONDS_IN_MINUTE, 2), IntervalUnit.MIN)

    return Interval(round(v / SECONDS_IN_HOUR, 2), IntervalUnit.H)


def infer_interval(a: datetime, b: datetime) -> Interval:
    # Calculate the interval between two datetime

    delta = b - a if b > a else a - b
    return infer_interval_by(delta)


def infer_interval_by(delta: timedelta) -> Interval:
    if delta.days:
        return infer_interval_in_days(delta.days)

    if delta.seconds:
        return infer_interval_in_seconds(delta.seconds)

    return Interval(int(delta.microseconds / 1000), IntervalUnit.MS)
