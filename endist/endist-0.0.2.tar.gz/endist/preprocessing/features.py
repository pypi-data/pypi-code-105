import pandas as pd
import numpy as np

def get_feats_smart_meter(s, mm_id, Pinst, max_threshold=1.3, resample=True, time_interval="15min"):
    """
    Get features for a single sample. 
    The input series is resampled to 15 minute intervals.
    
    The features are:
    - below_zero_perc
    - above_Pinst_perc
    - missing_values_perc
    - invalid_perc

    - duplic_count
    - max_duplic_per_day_count

    - invalid_timestamps_count
    - invalid_timestamps_perc
    - missing_timestamps_count
    - missing_timestamps_perc

    - missing_days_count
    - missing_days_perc
    
    Parameters
    ----------
    s : pandas.Series
        Sample.
    mm_id : str
        Meter ID.
    Pinst : float
        Connected power by the consumer owning the smart meter.
    max_threshold : float
        Maximum threshold for the power.
    resample : bool
        If True, the input series is resampled to the "time_interval" intervals (default: 15min).
    time_interval : str
        Time interval for resampling.

    Returns
    -------
    feats : dict
        Dictionary containing the features.
    
    Example
    -------
    >>> get_feats_smart_meter(s, mm_id, Pinst)
    """
    max_threshold = max_threshold
    # Resample to 15 minute intervals
    if resample:
        s_resampled = s.resample(time_interval).mean()
    else:
        s_resampled = s

    # VALIDATING VALUES
    below_zero_mask = (s_resampled.fillna(0) < 0).rename("below_zero")
    above_Pinst_mask = (s_resampled.fillna(0) > max_threshold*Pinst).rename("above_Pinst")
    missing_values_mask = (s_resampled.isnull()).rename("missing_values")

    invalid_mask = (below_zero_mask + above_Pinst_mask + missing_values_mask).rename("invalid")

    # DUPLICATES
    s_duplic = s.index.duplicated()
    max_duplic_per_day_count = pd.Series(s_duplic, 
                                         index=s.index).astype(np.int32).resample("1d").sum().max()

    # TIMESTAMPS
    invalid_timestamps_mask = (s.index.round("15min") != s.index)
    missing_timestamps_mask = s.fillna(0).resample("15min").mean().isnull()
    first_non_nan = s.dropna().index[0] if len(s.dropna()) > 0 else None
    ts_len_days = (s.index[-1] - s.index[0]).days

    d = {"mm_id": mm_id,

        # VALIDATING
        "below_zero_perc": round(100 * below_zero_mask.mean(), 4),
        "above_Pinst_perc": round(100 * above_Pinst_mask.mean(), 4),
        "missing_values_perc": round(100 * missing_values_mask.mean(), 4),
        "invalid_perc": round(100 * invalid_mask.mean(), 4),

        # DUPLICATES
        "duplic_count": s_duplic.sum(),
        "max_duplic_per_day_count": max_duplic_per_day_count,

        # OTHER STATS
        "Max": round(s.max(), 3),
        "Max_norm": round(s.max() / Pinst, 3),

        # TIMESTAMPS
        "first_ts": s.index[0],
        "first_not_nan": first_non_nan,
        "last_ts": s.index[-1],
        "ts_len_days": ts_len_days,

        "invalid_timestamps_count": invalid_timestamps_mask.sum(),
        "invalid_timestamps_perc": round(100 * invalid_timestamps_mask.mean(), 4),
        "missing_timestamps_count": missing_timestamps_mask.sum(),
        "missing_timestamps_perc": round(100 * missing_timestamps_mask.mean(), 4),
         
        # MISSING DAYS, WEEKS etc.
        "missing_days_count": (s_resampled.isnull().resample("1d").sum() == 96).sum(),
        "missing_days_perc": round(100 * s_resampled.isnull().resample("1d").mean().sum() / ts_len_days, 4)
    }
    return pd.Series(d)

