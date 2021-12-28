import matplotlib.pyplot as plt
from numpy import ndarray
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import adfuller
from typing import Callable


def print_p_value(
    series: ndarray
) -> None:
    """Show p-value of series.

    Parameters
    ----------
    series : pandas.core.series.Series
        Series to calculate and print p-value  

    Returns
    -------
    None
    """

    p_value = adfuller(series)[1]
    print('p-value: {} ({} than 0.05)'.format(
        round(p_value, 4),
        'less' if p_value < 0.05 else 'greater'))


def check_hypophysis(
        original_series: ndarray,
        transform_fun: Callable,
        orig_name: str,
        trans_name: str
) -> ndarray:
    """Show plots and p-value to analyze stationary of series.
    Dickey — Fuller test.

    Parameters
    ----------
    original_series : pandas.core.series.Series
        Series to check stationary 
    transform_fun : Callable
        Function which is suppose to make the series stationary
    orig_name : str
        Name of original series to show on plots' labels
    trans_name : str
        Name of transformed series to show on plots' labels

    Returns
    -------
    transformed_series : pandas.core.series.Series
        Transformed series
    """

    transformed_series = transform_fun(original_series)

    plt.subplots(nrows=3, ncols=1, constrained_layout=True, figsize=(11, 14))
    # Original series plot
    ax = plt.subplot(311)
    ax.set_title('Original')
    ax.set_ylabel(orig_name, rotation=0, labelpad=30)
    original_series.plot(ax=ax)

    # Transformed series plot
    ax = plt.subplot(312)
    ax.set_title('Transformed')
    ax.set_ylabel(trans_name, rotation=0, labelpad=30)
    transformed_series.plot(ax=ax)

    # Correlogram of original series
    ax = plt.subplot(313)
    plot_acf(transformed_series[1:], lags=30, ax=ax)

    # Show head of transformed series
    print(transformed_series.head(7))
    # p_value of original series
    print_p_value(transformed_series)

    return transformed_series
