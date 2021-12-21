import math
import random
import warnings
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
warnings.filterwarnings("ignore")
from visart import plot

def show_examples():
    """Show the plots examples"""
    fig, (ax_1, ax_2) = plt.subplots(2, 2, figsize=(15,20))
    ax1, ax2 = ax_1
    ax3, ax4 = ax_2

    x = list(range(1950, 1959))
    y = [164, 241, 234, 211, 122, 186, 183, 147, 143]
    hist_data = np.random.rand(3000) * 45.34
    bar_data = [10, 20, 30, 10, 50]
    bar_labels = ['Madrid', 'London', 'Tokyo', 'Sidney', 'Paris']

    p1 = plot(plot_type='scatter', fig=fig, ax=ax1, width=20, height=12)
    ax1.set_title("plot_type='scatter'")
    p1.add_data(x, y)
    p1.set_axis_labels('year', 'density')
    p1.show()

    p2 = plot(plot_type='line', fig=fig, ax=ax2, width=20, height=12)
    ax2.set_title("plot_type='line'")
    p2.add_data(x, y)
    p2.set_axis_labels('year', 'volume')
    p2.show()

    p3 = plot(plot_type='hist', fig=fig, ax=ax3, width=20, height=12)
    ax3.set_title("plot_type='hist'")
    p3.add_data(hist_data)
    p3.show()

    p4 = plot(plot_type='bar', fig=fig, ax=ax4, width=20, height=12, labels=bar_labels)
    ax4.set_title("plot_type='bar'")
    p4.add_data(bar_data)
    p4.show()
