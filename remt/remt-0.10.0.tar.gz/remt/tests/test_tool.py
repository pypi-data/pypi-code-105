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
Drawing tool unit tests.
"""

import operator

from remt import tool
from remt.data import Stroke, Segment

def test_group_line_segments():
    """
    Test grouping line segments.
    """
    items = [
        (0, 0, 1),
        (1, 1, 1),
        (2, 2, 2),
        (3, 3, 3),
        (4, 4, 3),
        (5, 5, 3),
        (6, 6, 4),
        (7, 7, 4),
        (8, 8, 4),
    ]
    s1, s2, s3, s4 = tool.group_line_segments(items, operator.itemgetter(2))
    assert (1, [(0, 0), (1, 1), (2, 2)]) == s1
    assert (2, [(2, 2), (3, 3)]) == s2
    assert (3, [(3, 3), (4, 4), (5, 5), (6, 6)]) == s3
    assert (4, [(6, 6), (7, 7), (8, 8)]) == s4

def test_group_line_segments_end_point():
    """
    Test grouping line segments with single point at the end.
    """
    items = [
        (0, 0, 1),
        (1, 1, 1),
        (2, 2, 2),
        (3, 3, 3),
        (4, 4, 3),
        (5, 5, 3),
        (6, 6, 0),
    ]
    s1, s2, s3 = tool.group_line_segments(items, operator.itemgetter(2))
    assert (1, [(0, 0), (1, 1), (2, 2)]) == s1
    assert (2, [(2, 2), (3, 3)]) == s2
    assert (3, [(3, 3), (4, 4), (5, 5), (6, 6)]) == s3

def test_group_line_segments_empty():
    """
    Test grouping line segments with empty input.
    """
    items = tool.group_line_segments([], operator.itemgetter(2))
    assert next(items, None) is None

def test_line_const():
    """
    Test calculation line with constant width and pressure.
    """
    stroke = Stroke(
        0, 0, 0, 10,
        [
            create_segment(0, 0, 100, 0),
            create_segment(1, 1, 100, 0),
            create_segment(2, 2, 100, 0),
        ]
    )
    calc = lambda v: v.width * 2
    items = tool.line_const(calc, stroke)
    result = next(items)

    assert next(items, None) is None

    assert 20 == result.width
    assert 1 == result.pressure
    assert [(0, 0), (1, 1), (2, 2)] == result.points

def test_line_var_pressure():
    """
    Test calculation of line with constant width and varying pressure.
    """
    stroke = Stroke(
        0, 0, 0, 10,
        [
            create_segment(0, 0, 100, 0.1),
            create_segment(1, 1, 100, 0.2),
            create_segment(2, 2, 100, 0.2),
            create_segment(3, 3, 100, 0.2),
            create_segment(4, 4, 100, 0.3),
            create_segment(5, 5, 100, 0),
        ]
    )
    calc = lambda st: st.width * 2
    l1, l2, l3 = tool.line_var_pressure(calc, stroke)

    assert 20 == l1.width
    assert 20 == l2.width
    assert 20 == l3.width

    assert 10 == l1.pressure
    assert 20 == l2.pressure
    assert 30 == l3.pressure

    assert [(0, 0), (1, 1)] == l1.points
    assert [(1, 1), (2, 2), (3, 3), (4, 4)] == l2.points
    assert [(4, 4), (5, 5)] == l3.points

def create_segment(x, y, width, pressure):
    return Segment(0, x, y, 0, 0, width, pressure)

# vim: sw=4:et:ai
