import pandas as pd
import numpy as np

def ahead_behind_fill(s_in, fill_mask=True, time_interval="15min"):
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
    >>> ahead_behind_fill(s_in)
    """
    print(pd.infer_freq(s_in.index))
    if "15" not in pd.infer_freq(s_in.index):
        raise ValueError(f"The input series MUST be at {time_interval} intervals.")
        
    s = s_in.copy()
    nan_mask = s.isnull()

    s_mean = pd.concat([s,
                        s.shift(-7*96),
                        s.shift(7*96),
                        s.shift(-14*96), 
                        s.shift(14*96),
                       ], axis=1).mean(axis=1, skipna=True)
    #if the value is missing and is in fill_mask, fill it with the mean of the values in the 1 and 2 weeks ahead and behind
    s.loc[fill_mask & nan_mask] = s_mean.loc[nan_mask]
    return s

#fill missing values in a series using mean
def mean_fill(s_in, fill_mask=True, time_interval="15min"):
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
    >>> ahead_behind_fill(s_in)
    """
    print(pd.infer_freq(s_in.index))
    if "15" not in pd.infer_freq(s_in.index):
        raise ValueError(f"The input series MUST be at {time_interval} intervals.")

    s = s_in.copy()
    nan_mask = s.isnull()
    #fill missing values using mean values
    s.loc[fill_mask & nan_mask] = s.mean()
    return s