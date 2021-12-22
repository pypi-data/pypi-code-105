#
# remt - note-taking support tool for reMarkable tablet
#
# Copyright (C) 2018-2021 by Artur Wroblewski <wrobell@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Drawing tool calculations.

Drawing tools characteristics is as follows

+-------------------+----------+------+-------------------+
| Tool              | Pressure | Tilt |      Brush        |
+===================+==========+======+===================+
| Ballpoint         |    Y     |  N   |        Y          |
+-------------------+----------+------+-------------------+
| Fineliner         |    N     |  N   |        N          |
+-------------------+----------+------+-------------------+
| Marker            |    N     |  Y   |      marker       |
+-------------------+----------+------+-------------------+
| Pencil            |    Y     |  Y   |      pencil       |
+-------------------+----------+------+-------------------+
| Mechanical pencil |   Y (1)  |  N   | pencil-mechanical |
+-------------------+----------+------+-------------------+
| Paintbrush        |    Y     |  Y   |        N          |
+-------------------+----------+------+-------------------+
| Highlighter       |    N     |  N   |        N          |
+-------------------+----------+------+-------------------+
| Caligraphy        |    N     |  Y   |        N          |
+-------------------+----------+------+-------------------+
| Eraser            |    N     |  N   |        N          |
+-------------------+----------+------+-------------------+
| Erase Area        |    N     |  N   |        N (3)      |
+-------------------+----------+------+-------------------+

1. Mechanical pencil uses pressure to distinguish between two brush
   versions - lighter or darker.
2. Highlighter has static width of 30px.
3. Some shapes have an irregular edge, could it be due to a brush?

Use transparent color for highlighter tool only. All other tools should use
appropriate brushes at full opacity. For example, drawing with pencil in
exactly the same place does not make it darker. This allows to draw a
single stroke of varying width with multiple lines in Cairo, which does not
support single line of varying width.

Certain formulas are adapted from

   https://github.com/Wacom-Developer/sdk-for-ink-android/

"""

import cytoolz.itertoolz as itz  # type: ignore
import cytoolz.functoolz as ftz  # type: ignore
import math
import operator
import typing as tp
from functools import partial
from itertools import groupby

from . import data as rdata

T = tp.TypeVar('T')
V = tp.TypeVar('V')

PI_2 = math.pi / 2

LineConstWidthCalc = tp.Callable[[rdata.Stroke], float]
LineVarWidthCalc = tp.Callable[[rdata.Stroke, rdata.Segment], float]

def line_const(calc: LineConstWidthCalc, stroke: rdata.Stroke) \
        -> tp.Iterable[rdata.LinePath]:
    """
    Return collection of lines of constant width and pressure between
    segments.

    :param calc: Width calculator.
    :param stroke: Stroke data to convert to line.
    """
    width = calc(stroke)
    segments = stroke.segments
    to_point = tp.cast(
        tp.Callable[[tp.Tuple[float, ...]], rdata.Point],
        operator.attrgetter('x', 'y')
    )

    points = [to_point(s) for s in segments]

    # set pressure to 1 as line is pressure insensitive
    yield rdata.LinePath(width, 1, points)

def line_var_pressure(calc: LineConstWidthCalc, stroke: rdata.Stroke) \
        -> tp.Iterable[rdata.LinePath]:
    """
    Return collection of lines of constant width, but varying pressure
    between segments.

    :param calc: Width calculator.
    :param stroke: Stroke data to convert to line.
    """
    width = calc(stroke)
    segments = stroke.segments
    create_line = partial(rdata.LinePath, width)
    key = tp.cast(
        tp.Callable[[tp.Tuple[float, ...]], int],
        operator.itemgetter(2)
    )

    # extract positions and optimize by pressure level
    items = ((s.x, s.y, pressure_level(s)) for s in segments)
    by_pressure = group_line_segments(items, key)

    lines = (create_line(p, pt) for p, pt in by_pressure)
    yield from lines

def line_var_width_pressure(calc: LineVarWidthCalc, stroke: rdata.Stroke) \
        -> tp.Iterable[rdata.LinePath]:
    """
    Return collection of lines having varying width or varying pressure
    between segments.

    :param calc: Width calculator.
    :param stroke: Stroke data to convert to line.
    """
    segments = stroke.segments

    # convert width to key; by rounding at 3rd decimal place we shall still
    # get more than 1200 dpi out of it
    key_width = ftz.compose(
        int,
        partial(operator.mul, 1000),
        partial(calc, stroke),
    )

    # extract width and pressure
    key = tp.cast(
        tp.Callable[[tp.Tuple[float, ...]], tp.Tuple[int, int]],
        operator.itemgetter(2, 3)
    )

    items = ((s.x, s.y, key_width(s), pressure_level(s)) for s in segments)
    groups = group_line_segments(items, key)
    lines = (rdata.LinePath(w / 1000, p, pt) for (w, p), pt in groups)
    yield from lines

def group_line_segments(segments: tp.Iterable[T], key: tp.Callable[[T], V]) \
        -> tp.Iterable[tp.Tuple[V, rdata.Points]]:
    """
    Group line segments using key function.
    """
    to_points = ftz.compose(list, partial(itz.pluck, [0, 1]))

    items = groupby(segments, key)
    by_key = [(k, to_points(v)) for k, v in items]
    if not by_key:
        return

    # yield each segment; add first point of next segment to the current
    # segment
    pairs = itz.sliding_window(2, by_key)
    result = ((k, pt + pt_n[:1]) for (k, pt), (_, pt_n) in pairs)
    yield from result

    # if last segment is not just a point, then return it as well
    last = by_key[-1]
    if len(last[1]) > 1:
        yield last

def pressure_level(segment: rdata.Segment) -> int:
    """
    Calculate pressure level for a stroke segment.
    """
    return min(99, int(segment.pressure * 100))

def calc_width_fineliner(stroke: rdata.Stroke) -> float:
    """
    Calculate fineliner width.

    :param stroke: Stroke data.
    """
    return calc_width_standard(stroke)

def calc_width_marker(stroke: rdata.Stroke, segment: rdata.Segment) -> float:
    """
    Calculate marker tool width.
    """
    return calc_width_tilt(segment) + 0.5

def calc_width_pencil(stroke: rdata.Stroke, segment: rdata.Segment) -> float:
    """
    Calculate marker tool width.
    """
    return calc_width_tilt(segment) + 0.5

def calc_width_painbrush(stroke: rdata.Stroke, segment: rdata.Segment) \
        -> float:
    """
    Calculate marker tool width.
    """
    width = calc_width_tilt(segment) + 0.5
    return apply_pressure(segment, width)

def calc_width_mechanical_pencil(stroke: rdata.Stroke) -> float:
    """
    Calculate mechanical pencil width.

    :param stroke: Stroke data.
    """
    return 16 * stroke.width - 27

def calc_width_eraser(stroke: rdata.Stroke) -> float:
    """
    Calculate eraser width.

    :param stroke: Stroke data.
    """
    return 1280 * stroke.width ** 2 - 4800 * stroke.width + 4510

def calc_width_ballpoint(stroke: rdata.Stroke, segment: rdata.Segment) \
        -> float:
    """
    Calculate ballpoint tool line width.

    :param stroke: Stroke data.
    :param segment: Segment data.
    """
    width = calc_width_standard(stroke)
    return apply_pressure(segment, width)

def calc_width_caligraphy(stroke: rdata.Stroke, segment: rdata.Segment) \
        -> float:
    """
    Calculate caligraphy tool line width.

    :param stroke: Stroke data.
    :param segment: Segment data.
    """
    return calc_width_tilt(segment)

def calc_width_standard(stroke: rdata.Stroke) -> float:
    """
    Calculate width for a tool without tilt.

    :param stroke: Stroke data.
    """
    return 32 * stroke.width ** 2 - 116 * stroke.width + 107

def calc_width_tilt(segment: rdata.Segment) -> float:
    """
    Calculate width for a tool with tilt applied.

    :param segment: Segment data.
    """
    return segment.width / PI_2 * 1.5

def apply_pressure(segment: rdata.Segment, width: float) -> float:
    """
    Apply pressure to the width of a tool.

    :param segment: Segment data.
    :param width: Width to be changed by pressure.
    """
    return width + segment.pressure ** 2048

line_unknown = partial(line_const, lambda s: rdata.PEN_WIDTH_UKNOWN)
line_ballpoint = partial(line_var_width_pressure, calc_width_ballpoint)
line_fineliner = partial(line_const, calc_width_fineliner)
line_marker = partial(line_var_width_pressure, calc_width_marker)
line_pencil = partial(line_var_width_pressure, calc_width_pencil)
line_mechanical_pencil = partial(
    line_var_pressure, calc_width_mechanical_pencil
)
line_paintbrush = partial(line_var_width_pressure, calc_width_painbrush)
line_highlighter = partial(line_const, lambda s: rdata.PEN_WIDTH_HIGHLIGHTER)
line_caligraphy = partial(line_var_width_pressure, calc_width_caligraphy)
line_eraser = partial(line_const, calc_width_eraser)
line_erase_area = partial(line_const, lambda s: rdata.PEN_WIDTH_ERASE_AREA)

# vim: sw=4:et:ai
