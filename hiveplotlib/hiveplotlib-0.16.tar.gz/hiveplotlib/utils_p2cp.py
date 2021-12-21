# Gary Koplik
# gary<dot>koplik<at>geomdata<dot>com
# December, 2021
# utils_p2cp.py


"""
Utility functions for building Polar Parallel Coordinate Plots.
"""


import pandas as pd
from typing import Hashable


def indices_for_unique_values(df: pd.DataFrame, column: Hashable):
    """
    Find the indices corresponding to each unique value in a column of a ``pandas`` dataframe.

    :param df: dataframe from which to find index values.
    :param column: column of the dataframe to use to find indices corresponding to each of the column's unique values.
    :return: ``dict`` whose keys are the unique values in the column of data and whose values are 1d arrays of index
        values.
    """

    return df.groupby(column).indices
