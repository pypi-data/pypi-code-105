
import pandas as pd

def read_smart_meter_data(path, sep=",",index_col=0, parse_dates=True):
    """
    Read smart meter data from csv file.
    
    the format of the input data should be:
    datetime,value1,value2,value3

    Parameters
    ----------
    path : str
        Path to the csv file.
    sep : str
        Separator in the csv file.
    index_col : int
        Index of the column that will be used as index.
    parse_dates : bool
        If True, the index will be parsed as datetime.
    
    Returns
    -------
    df : pandas.DataFrame

    Example
    -------
    >>> read_smart_meter_data("data/smart_meter_data.csv", sep=",", index_col=0, parse_dates=True)
    """

    # Import data
    df = pd.read_csv(path, sep=sep, index_col=index_col, parse_dates=parse_dates)
    df.index = pd.to_datetime(df.index)

    return df

def read_pickle(path):
    """
    Read pickle file containing a pandas.DataFrame.
    
    Parameters
    ----------
    path : str
        Path to the pickle file.
    
    Returns
    -------
    df : pandas.DataFrame

    Example
    -------
    >>> read_pickle("data/smart_meter_data.pkl")
    """

    # Import data
    df = pd.read_pickle(path)

    return df