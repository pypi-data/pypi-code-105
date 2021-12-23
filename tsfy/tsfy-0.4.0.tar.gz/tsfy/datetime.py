from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

from dateutil.relativedelta import relativedelta


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


def infer_interval(a: datetime, b: datetime) -> Interval:
    # Calculate the interval between two datetime

    delta = relativedelta(b, a) if b > a else relativedelta(a, b)
    return infer_interval_by(delta)


def infer_interval_by(delta: relativedelta) -> Interval:
    if delta.years:
        return Interval(delta.years, IntervalUnit.Y)

    if delta.months:
        return Interval(delta.months, IntervalUnit.M)

    if delta.days:
        return Interval(delta.days, IntervalUnit.D)

    if delta.hours:
        return Interval(delta.hours, IntervalUnit.H)

    if delta.minutes:
        return Interval(delta.minutes, IntervalUnit.MIN)

    if delta.seconds:
        return Interval(delta.seconds, IntervalUnit.S)

    return Interval(int(delta.microseconds / 1000), IntervalUnit.MS)
