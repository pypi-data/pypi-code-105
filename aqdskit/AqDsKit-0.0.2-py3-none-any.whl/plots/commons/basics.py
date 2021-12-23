from matplotlib import pyplot as plt


def plot_multiple_ys_against_x(
        ax,
        x,
        ys_dict: dict,
        ys_dict_r: dict = None,
        x_label: str = 'xs',
        y_label: str = 'y',
        y_label_r: str = 'y_r',
        title: str = "Untitled - Multiple Xs vs. Y",
        title_fontsize: str = "large",
        text_fontsize: str = "medium",
        show_grid: bool = True,
        show_legend: bool = True,
    ):
    """plot multiple Y values against same X-axis on the given ax

    :param ax: given ax to plot on, figure size is predefined in ax, fig
    :param x: array-like, x-axis values
    :param ys_dict: dictionary of several ys and their names {y_name : y_values} on the main (left) y_axis
    :param ys_dict_r: dictionary of several ys and their names {y_name : y_values} on the twin (right) y_axis
    :param x_label: label to show for x axis
    :param y_label: label to show for y axis on the main (left) ax
    :param y_label_r: label to show for y axis on the twin (right) ax
    :param title: title for the chart
    :param title_fontsize:
    :param text_fontsize:
    :param show_grid: whether to show grid
    :param show_legend: whether to show legend of different y names

    :return: ax of the plotted chart
    """

    for y_name, y in ys_dict.items():
        ax.plot(x, y, marker = 'o', label = y_name, lw = 2)

    ax.set_title(title, fontsize = title_fontsize)

    ax.set_xlabel(x_label, fontsize = text_fontsize)
    ax.set_ylabel(y_label, fontsize = text_fontsize)
    ax.tick_params(labelsize = text_fontsize)

    if show_grid:
        ax.grid(True)
    if show_legend:
        ax.legend()

    if ys_dict_r:
        #ax2_color = '#939b95'
        ax2 = ax.twinx()

        for y_name, y in ys_dict_r.items():
            ax2.plot(x, y, linestyle = ':', label = y_name, lw = 2)
       # ax2.plot(x, times, linestyle = ':', alpha = 0.8)
        ax2.set_ylabel(y_label_r, fontsize = text_fontsize)
        ax2.tick_params(labelsize = text_fontsize)