import math

def plan_plot_grid(n_plots: int) -> tuple:
    """find optimal placement (rows, cols) for given number of plots to place
    => min{rows - cols}  s.t. cols^2 <= n_plots <= rows^2 and cols * rows >= n_plots

    :param n_plots: number of plots to place
    :return: optimal (rows, cols)
    """
    rows = math.ceil(n_plots ** 0.5)
    cols = math.ceil(n_plots / rows)
    return rows, cols


def plot_walker(n_plots: int):
    """a generator which yields each step of row anc col number to place the plot,
    given total number of plots in the grid

    :param n_plots:
    :return: a generator of next plot loc (row and column)
    """
    rows, cols = plan_plot_grid(n_plots)  # get the placement grid size
    r, c = 0, 0
    for i in range(n_plots):
        yield r, c
        if c + 1 >= cols:
            # if current row is full, move to next row
            r += 1
            c = 0
        else:
            c += 1

def ax_walker(n_plots: int, axes):
    """a generator which yields each step of ax to place the plot

    :param n_plots: total number of plots in the grid
    :param axes: created by: fig, axes = plt.subplots(rows, cols, figsize = figsize)
    :return: a generator of next plot ax
    """
    rows, cols = plan_plot_grid(n_plots)
    if n_plots == 1:
        yield axes  # only single ax is contained in axes, return the single ax back

    elif rows == 1 or cols == 1:
        # it will still be a 1D array of ax, so only iterate along one dimension
        for ax in axes:
            yield ax
    else:
        # else its a 2D plot (have row and col > 1, the axes will be a 2D array)
        r, c = 0, 0
        for i in range(n_plots):
            yield axes[r, c]
            if c + 1 >= cols:
                # if current row is full, move to next row
                r += 1
                c = 0
            else:
                c += 1