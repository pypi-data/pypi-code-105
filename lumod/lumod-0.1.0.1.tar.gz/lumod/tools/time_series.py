# -*- coding: utf-8 -*-
"""
Tools for time series processing

Author:
Saul Arciniega Esparza
Hydrogeology Group, Faculty of Engineering,
National Autonomous University of Mexico
zaul.ae@gmail.com | sarciniegae@comunidad.unam.mx
"""

import os
import numpy as np
import pandas as pd


FILEPATH = os.path.dirname(os.path.abspath(__file__))
MAINPATH = os.path.dirname(FILEPATH)

# ==============================================================================
# Time series aggregation
# ==============================================================================

def monthly_aggregation(data, method="sum"):
    """
    Monthly aggregation

    :param data:     [Serie, DataFrame] input timeserie
    :param method:   [str] aggregation method ("sum", "mean")
    :return:         [Serie, DataFrame] output monthly serie
    """
    if method.lower() == "sum":
        data_m = data.resample("1M").sum()
    else:
        data_m = data.resample("1M").mean()
    data_m.index = data_m.index - pd.offsets.MonthBegin()
    return data_m


def daily_stats(data):
    """
    Computes the daily mean by day of year.
    Ignores Feb 29.

    :param data:     [Serie, DataFrame] input timeserie
    :return:         [Serie, DataFrame] output mean daily value
    """
    mask = (data.index.month == 2) & (data.index.day == 29)
    data = data.loc[~mask]
    stats = pd.DataFrame(
        np.zeros((365, 7)),
        index=np.arange(1, 366, dtype=int),
        columns=["mean", "std", "min", "X25", "X50", "X75", "max"]
    )
    stats["mean"] = data.groupby(data.index.day).mean()
    stats["std"] = data.groupby(data.index.day).std()
    stats["min"] = data.groupby(data.index.day).min()
    stats["X25"] = data.groupby(data.index.day).quantile(0.25)
    stats["X50"] = data.groupby(data.index.day).quantile(0.50)
    stats["X75"] = data.groupby(data.index.day).quantile(0.75)
    stats["max"] = data.groupby(data.index.day).min()
    return stats


def monthly_stats(data, method="mean"):
    """
    Computes the monthly mean time serie from daily timeseries

    :param data:     [Serie, DataFrame] input timeserie
    :param method:   [str] monthly aggregation method ("sum", "mean", None).
                        Use None when then input data is in monthly time scale
    :return:         [Serie, DataFrame] output mean monthly value
    """
    if method is None:
        data_m = data.copy()
    else:
        method = method.lower()
        if method == "sum":
            data_m = data.resample("1M").sum()
        elif method == "mean":
            data_m = data.resample("1M").mean()
    stats = pd.DataFrame(
        np.zeros((12, 7)),
        index=np.arange(1, 13, dtype=int),
        columns=["mean", "std", "min", "X25", "X50", "X75", "max"]
    )
    stats["mean"] = data_m.groupby(data_m.index.month).mean()
    stats["std"] = data_m.groupby(data_m.index.month).std()
    stats["min"] = data_m.groupby(data_m.index.month).min()
    stats["X25"] = data_m.groupby(data_m.index.month).quantile(0.25)
    stats["X50"] = data_m.groupby(data_m.index.month).quantile(0.50)
    stats["X75"] = data_m.groupby(data_m.index.month).quantile(0.75)
    stats["max"] = data_m.groupby(data_m.index.month).min()
    return stats


# ==============================================================================
# Hydrological indices
# ==============================================================================

def flow_duration_curve(qt):
    """
    Returns the flow duration curve (FDC) from daily streamflow time series

    :param qt:       [Serie, DataFrame] input timeserie
    :return:         [Serie, DataFrame] output FDC
    """
    qt_sort = qt.sort_values(ascending=False)
    n = len(qt_sort)
    qt_sort.index = np.arange(n) / n
    return qt_sort


# ==============================================================================
# Data Processing
# ==============================================================================

def load_example(n):
    """
    Load forcings for timseries examples
    """
    filename = os.path.join(MAINPATH, "data", f"example{n}.csv")
    attrsfile = os.path.join(MAINPATH, "data", "attributes.csv")
    if os.path.exists(filename):
        attrs = pd.read_csv(attrsfile, index_col=[0])
        data = pd.read_csv(filename, index_col=[0], parse_dates=[0])
        return attrs.loc[n, :], data
    else:
        raise ValueError("Wrong example file number! Try with other number.")


