# Author: Nicolas Legrand <nicolas.legrand@cfin.au.dk>

from typing import Dict, Optional

import numpy as np
import pandas as pd
from bokeh.layouts import column
from bokeh.models import BoxAnnotation, CDSView, Circle, IndexFilter, Line, Range1d
from bokeh.models.tools import HoverTool, RangeTool
from bokeh.plotting import ColumnDataSource, figure
from bokeh.plotting.figure import Figure


def plot_rr(
    rr: np.ndarray,
    unit: str = "rr",
    kind: str = "cubic",
    line: bool = True,
    points: bool = True,
    artefacts: Optional[Dict[str, np.ndarray]] = None,
    input_type: str = "peaks",
    show_limits: bool = True,
    slider: bool = True,
    ax=None,
    figsize: int = 200,
) -> Figure:
    """Plot continuous or discontinuous RR intervals time series.

    Parameters
    ----------
    rr : np.ndarray
        1d numpy array of RR intervals (in seconds or miliseconds) or peaks
        vector (boolean array).
    unit : str
        The heart rate unit in use. Can be `'rr'` (R-R intervals, in ms)
        or `'bpm'` (beats per minutes). Default is `'rr'`.
    kind : str
        The method to use (parameter of `scipy.interpolate.interp1d`). The
        possible relevant methods for instantaneous heart rate are `'cubic'`
        (defalut), `'linear'`, `'previous'` and `'next'`.
    line : bool
        If `True`, plot the interpolated instantaneous heart rate.
    points : bool
        If `True`, plot each peaks (R wave or systolic peaks) as separated
        points.
    artefacts : dict
        Dictionnary storing the parameters of RR artefacts rejection.
    input_type : str
        The type of input vector. Can be `"peaks"`, `"peaks_idx"`, `"rr_ms"`,
        or `"rr_s"`. Default to `"peaks"`.
    show_limits : bool
        Use shaded areas to represent the range of physiologically impossible R-R
        intervals. Defaults to `True`.
    slider : bool
        If `True`, add a slider to zoom in/out in the signal (only working with
        bokeh backend).
    ax : None
        Only relevant when using `backend="matplotlib"`.
    figsize : int
        The height of the figure. Default is `200`.

    Returns
    -------
    fig : :class:`bokeh.plotting.figure.Figure`
        The bokeh figure containing the plot.

    """

    ylabel = "R-R interval (ms)" if unit == "rr" else "Beats per minute (bpm)"

    p1 = figure(
        title="Instantaneous heart rate",
        sizing_mode="stretch_width",
        plot_height=figsize,
        x_axis_label="Time",
        x_axis_type="datetime",
        y_axis_label=ylabel,
        output_backend="webgl",
        tools="pan,wheel_zoom,box_zoom,box_select,reset,save",
    )

    # Instantaneous Heart Rate - Peaks
    if input_type == "rr_ms":
        ibi = np.array(rr)
        rr_idx = pd.to_datetime(np.cumsum(ibi), unit="ms", origin="unix")
    elif input_type == "rr_s":
        ibi = np.array(rr) * 1000
        rr_idx = pd.to_datetime(np.cumsum(ibi), unit="ms", origin="unix")
    elif input_type == "peaks":
        ibi = np.diff(np.where(rr)[0])
        rr_idx = pd.to_datetime(np.where(rr)[0][1:], unit="ms", origin="unix")
    elif input_type == "peaks_idx":
        ibi = np.diff(rr)
        rr_idx = pd.to_datetime(rr[1:], unit="ms", origin="unix")

    if artefacts is None:
        outliers = np.zeros(len(ibi), dtype=bool)
    else:
        outliers = (
            artefacts["ectopic"]
            | artefacts["short"]
            | artefacts["long"]
            | artefacts["extra"]
            | artefacts["missed"]
        )

    points_source = ColumnDataSource(
        data=dict(
            time=rr_idx,
            rr=ibi,
            bpm=60000 / ibi,
            nbeat=np.arange(1, len(rr_idx) + 1),
            outliers=outliers,
        )
    )

    if line is True:

        # Instantaneous Heart Rate - Lines
        linePlot = Line(
            x="time",
            y=unit,
            line_color="#4c72b0",
        )
        p1.add_glyph(
            points_source,
            linePlot,
        )

    if points is True:

        # Normal RR intervals
        circlePlot = Circle(
            x="time",
            y=unit,
            size=6,
            fill_color="lightgrey",
            line_color="grey",
        )
        circlePlot_selected = Circle(
            x="time",
            y=unit,
            size=6,
            fill_color="firebrick",
            line_color="grey",
        )
        g1 = p1.add_glyph(
            points_source,
            circlePlot,
            hover_glyph=circlePlot_selected,
        )

        hover = HoverTool(
            renderers=[g1],
            tooltips=[
                ("time", "@time{:%M:%S.%3Ns}"),
                ("R-R interval", "@rr{%0.2f} ms"),
                ("BPM", "@bpm{%0.2f} BPM"),
                ("Heartbeat number", "@nbeat"),
            ],
            formatters={"@time": "datetime", "@rr": "printf", "@bpm": "printf"},
            mode="mouse",
        )

        if artefacts is not None:

            # Short RR intervals
            if artefacts["short"].any():
                short_view = CDSView(
                    source=points_source,
                    filters=[IndexFilter(np.where(artefacts["short"])[0])],
                )
                p1.circle(
                    x="time",
                    y=unit,
                    size=10,
                    legend_label="Short intervals",
                    fill_color="#c56c5e",
                    line_color="black",
                    source=points_source,
                    view=short_view,
                )

            # Long RR intervals
            if artefacts["long"].any():
                long_view = CDSView(
                    source=points_source,
                    filters=[IndexFilter(np.where(artefacts["long"])[0])],
                )
                p1.circle(
                    x="time",
                    y=unit,
                    size=10,
                    legend_label="Long intervals",
                    fill_color="#9ac1d4",
                    line_color="black",
                    source=points_source,
                    view=long_view,
                )

            # Missed RR intervals
            if artefacts["missed"].any():
                missed_view = CDSView(
                    source=points_source,
                    filters=[IndexFilter(np.where(artefacts["missed"])[0])],
                )
                p1.square(
                    x="time",
                    y=unit,
                    size=10,
                    legend_label="Missed intervals",
                    fill_color="#2f5f91",
                    line_color="black",
                    source=points_source,
                    view=missed_view,
                )

            # Extra RR intervals
            if artefacts["extra"].any():
                extra_view = CDSView(
                    source=points_source,
                    filters=[IndexFilter(np.where(artefacts["extra"])[0])],
                )
                p1.square(
                    x="time",
                    y=unit,
                    size=10,
                    legend_label="Extra intervals",
                    fill_color="#9d2b39",
                    line_color="black",
                    source=points_source,
                    view=extra_view,
                )

            # Ectopic beats
            if artefacts["ectopic"].any():
                ectopic_view = CDSView(
                    source=points_source,
                    filters=[IndexFilter(np.where(artefacts["ectopic"])[0])],
                )
                p1.triangle(
                    x="time",
                    y=unit,
                    size=10,
                    legend_label="Ectopic beats",
                    fill_color="#6c0073",
                    line_color="black",
                    source=points_source,
                    view=ectopic_view,
                )

        # Add hover tool
        p1.add_tools(hover)

    # Show physiologically impossible ranges
    if show_limits is True:
        high, low = (3000, 200) if unit == "rr" else (300, 20)
        upper_bound = BoxAnnotation(bottom=high, fill_alpha=0.1, fill_color="red")
        p1.add_layout(upper_bound)
        lower_bound = BoxAnnotation(top=low, fill_alpha=0.1, fill_color="red")
        p1.add_layout(lower_bound)

    cols = (p1,)

    if slider is True:
        select = figure(
            title="Select the time window",
            y_range=p1.y_range,
            y_axis_type=None,
            plot_height=int(figsize * 0.5),
            x_axis_type="datetime",
            tools="",
            toolbar_location=None,
            background_fill_color="#efefef",
        )

        if line is True:
            select.line("time", unit, source=points_source)
            p1.x_range = Range1d(start=rr_idx[0], end=rr_idx[-1])
        else:
            select.circle("time", unit, source=points_source)
            p1.x_range = Range1d(start=rr_idx[0], end=rr_idx[-1])
        range_tool = RangeTool(x_range=p1.x_range)
        range_tool.overlay.fill_color = "navy"
        range_tool.overlay.fill_alpha = 0.2

        select.ygrid.grid_line_color = None
        select.add_tools(range_tool)
        select.toolbar.active_multi = range_tool

        cols += (select,)  # type: ignore

    if len(cols) > 1:
        return column(*cols, sizing_mode="stretch_width")
    else:
        return cols[0]
