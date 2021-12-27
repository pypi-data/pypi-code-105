import pandas as pd
import numpy as np

def ahead_behind_fill(s_in, fill_mask=False, time_interval="15T"):
    """
    Fill missing values in a series by using the values in the 1 and 2 weeks ahead and behind and calculating their mean.
    The input series MUST be at 15 minute intervals.

    Parameters
    ----------
    s_in : pandas.Series
        Input series.
    fill_mask : pandas.Series
        A boolean series of the same length as s_in, indicating which values to fill.
    time_interval : str
        The time interval of the input series.    

    Returns 
    -------
    s_out : pandas.Series
        Output series.

    Example
    -------
    >>> ahead_behind_fill(s_in)
    """
    infered_freq = pd.infer_freq(s_in.index)
    timestamps_in_day = 96
    if infered_freq != time_interval:
        if infered_freq == "15T" or infered_freq == "15min":
            timestamps_in_day = 96
        elif infered_freq == "10T" or infered_freq == "10min":
            timestamps_in_day = 144
        elif infered_freq == "30T" or infered_freq == "30min":
            timestamps_in_day = 48
        elif infered_freq == "60T" or infered_freq == "60min" or infered_freq == "1h" or infered_freq == "1H":
            timestamps_in_day = 24
        elif infered_freq == "D":
            timestamps_in_day = 1
        else:
            raise ValueError(f"The input series frequency ({infered_freq}) could not be processed.")

    s = s_in.copy()
    nan_mask = s.isnull()
    if fill_mask is False:
        fill_mask = s.transform(lambda _: True)
    s_mean = pd.concat([s,
                        s.shift(-7*timestamps_in_day),
                        s.shift(7*timestamps_in_day),
                        s.shift(-14*timestamps_in_day), 
                        s.shift(14*timestamps_in_day),
                       ], axis=1).mean(axis=1, skipna=True)
    #if the value is missing and is in fill_mask, fill it with the mean of the values in the 1 and 2 weeks ahead and behind
    s.loc[fill_mask & nan_mask] = s_mean.loc[nan_mask]
    return s

def mean_fill(s_in, fill_mask=False):
    """
    Fill missing values in a series by using the values in the 1 and 2 weeks ahead and behind and calculating their mean.
    The input series MUST be at 15 minute intervals.

    Parameters
    ----------
    s_in : pandas.Series
        Input series.
    fill_mask : pandas.Series
        A boolean series indicating which values to fill.
    time_interval : str
        The time interval of the input series.    

    Returns 
    -------
    s_out : pandas.Series
        Output series.

    Example
    -------
    >>> mean_fill(s_in)
    """
    s = s_in.copy()
    nan_mask = s.isnull()
    if fill_mask is False:
        fill_mask = s.transform(lambda _: True)
    #fill missing values using mean values
    s.loc[fill_mask & nan_mask] = s.mean()
    return s