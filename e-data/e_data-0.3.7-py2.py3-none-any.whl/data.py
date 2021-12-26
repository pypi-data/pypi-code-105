"""Data structures definition"""

from __future__ import annotations

import datetime
from collections.abc import Iterable
from typing_extensions import TypedDict
from copy import deepcopy

# DRAFT

"""Data types."""

class Supply (TypedDict):
    """Supplies data class"""
    cups: str
    start: datetime.datetime
    end: datetime.datetime
    address: str | None
    postal_code: str | None
    province: str | None
    municipality: str | None
    distributor: str | None
    point_type: str
    distributor_code: str

class Contract (TypedDict):
    """Contracts data class."""
    cups: str
    start: datetime.datetime
    end: datetime.datetime
    marketer: str
    distributor_code: int
    power_p1: float | None
    power_p2: float | None
    power_p3: float | None
    power_p4: float | None
    power_p5: float | None
    power_p6: float | None

class Consumption (TypedDict):
    """Consumption data class."""
    start: datetime.datetime
    end: datetime.datetime
    value_kwh: float
    real: bool

class MaxPower (TypedDict):
    """MaxPower data class."""
    start: datetime.datetime
    end: datetime.datetime
    time: datetime.datetime
    value_kw: float

class EnergyCost (TypedDict):
    """EnergyCost data class."""
    start: datetime.datetime
    end: datetime.datetime
    value_eur: float

class DatadisData (TypedDict):
    """Datadis data class"""
    supplies: Iterable [Supply]
    contracts: Iterable [Contract]
    consumptions: Iterable [Consumption]
    maximeter: Iterable [MaxPower]

class EsiosData (TypedDict):
    """Esios data class"""
    energy_costs: Iterable [EnergyCost]

"""Data handlers."""

def add_or_update (base_items: Iterable [dict], new_items: Iterable [dict], key):
    """Add or update dict in list"""
    new_list = deepcopy(base_items)
    nn = []
    for n in new_items:
        for o in new_list:
            if n[key] == o[key]:
                for i in o:
                    o[i] = n[i]
                break
        else:
            nn.append (n)
    new_list.extend(nn)
    return new_list

def prune_and_order (lst, dt_from: datetime.datetime, dt_to: datetime.datetime, gap_interval: datetime.timedelta = datetime.timedelta(hours=1), dt_key: str = "start"):
    """Filters, sorts, remove duplicates and find missing gaps"""
    
    # filter range
    _lst = [ x for x in deepcopy(lst) if dt_from <= x[dt_key] <= dt_to ]
    
    # sort by key
    _lst = sorted(_lst, key = lambda i: i[dt_key])
    
    # remove duplicates
    new_lst = []
    [
        new_lst.append(x) for x in _lst if x[dt_key] not in [ y[dt_key] for y in new_lst ]
    ]

    # find gaps
    gaps = []
    _last = dt_from
    for i in new_lst:
        if (i[dt_key] - _last) > gap_interval:
            gaps.append({"from": _last, "to": i[dt_key]})
        _last = i[dt_key]
    if (dt_to - _last) > gap_interval:
        gaps.append({"from": _last, "to": dt_to})

    return new_lst, gaps