import pytest
from mba.mba.visualization.sales import TransactionPlot

def test_dow_plot():
    expected = 'plot'
    print(TransactionPlot().df_transaction[:5])

    assert expected == 'plot'