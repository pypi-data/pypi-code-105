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
reMarkable strokes drawing using Cairo library.
"""

import cairo
import cytoolz.itertoolz as itz  # type: ignore
import io
import itertools
import logging
import os.path
import pkgutil
import typing as tp
from collections import defaultdict
from contextlib import contextmanager
from functools import singledispatch, partial
from itertools import accumulate

from . import const, tool
from . import data as rdata
from .pdf import pdf_scale, Poppler

logger = logging.getLogger(__name__)

ALPHA = 0.1

COLOR_STROKE = {
    rdata.ColorIndex.BLACK: rdata.Color(0, 0, 0, 1),
    rdata.ColorIndex.GREY: rdata.Color(0.5, 0.5, 0.5, 1),
    rdata.ColorIndex.WHITE: rdata.Color(1, 1, 1, 1),
    rdata.ColorIndex.BLUE: rdata.Color(0, 0.38, 0.79, 1),
    rdata.ColorIndex.RED: rdata.Color(0.85, 0.02, 0.2, 1),
    rdata.ColorIndex.YELLOW: rdata.Color(1, 0.81, 0.0, ALPHA),
    rdata.ColorIndex.GREEN: rdata.Color(0.66, 0.98, 0.36, ALPHA),
    rdata.ColorIndex.PINK: rdata.Color(1, 0.33, 0.81, ALPHA),
}

STYLE_DEFAULT = rdata.Style(
    tool.line_const,
    COLOR_STROKE[rdata.ColorIndex.BLACK],
    cairo.LINE_JOIN_ROUND,
    cairo.LINE_CAP_ROUND,
)
style_default = STYLE_DEFAULT._replace

STYLE_HIGHLIGHTER = rdata.Style(
    tool.line_highlighter,
    COLOR_STROKE[rdata.ColorIndex.YELLOW],
    cairo.LINE_JOIN_ROUND,
    cairo.LINE_CAP_BUTT,
)

STYLE_ERASER = rdata.Style(
    tool.line_eraser,
    COLOR_STROKE[rdata.ColorIndex.WHITE],
    cairo.LINE_JOIN_ROUND,
    cairo.LINE_CAP_ROUND,
)

STYLE_UNKNOWN_TOOL = style_default(tool_line=tool.line_unknown, dash=[1, 5])

path_brush = partial(os.path.join, 'brush')

@singledispatch
def draw(item: tp.Any, context: rdata.Context):
    raise NotImplementedError('Unknown item to draw: {}'.format(item))

@draw.register
def _page(page: rdata.Page, context: rdata.Context):
    surface = context.cr_surface
    page_number = next(context.page_number)
    if page_number:
        surface.show_page()

    if context.pdf_doc:
        # get page and set size of the current page of the cairo surface
        pdf_page = context.pdf_doc.get_page(page_number)
        w, h = pdf_page.get_size()
        surface.set_size(w, h)

        cr = context.cr_ctx
        # render for printing to keep the quality of the document
        pdf_page.render_for_printing(cr)

        # render remarkable lines data at scale to fit the document
        cr.save()  # to be restored at page end
        factor = pdf_scale(pdf_page)
        cr.scale(factor, factor)

@draw.register
def _page_end(page: rdata.PageEnd, context: rdata.Context):
    if context.pdf_doc:
        context.cr_ctx.restore()

@draw.register
def _layer(layer: rdata.Layer, context: rdata.Context):
    pass

@draw.register
def _stroke(stroke: rdata.Stroke, context: rdata.Context) -> None:
    style = context.style[stroke.pen]
    if style is STYLE_UNKNOWN_TOOL:
        logger.debug('Not supported pen for stroke: {}'.format(stroke))

    if stroke.color not in COLOR_STROKE:
        logger.debug('Unknown color index: {}'.format(stroke.color))
    if stroke.pen in (rdata.Pen.ERASER_AREA, rdata.Pen.ERASER):
        color = style.color
    else:
        color = COLOR_STROKE.get(stroke.color, rdata.ColorIndex.BLACK)

    cr = context.cr_ctx
    cr.save()

    draw_stroke = partial(draw_fill, cr) \
        if stroke.pen == rdata.Pen.ERASER_AREA else cr.stroke

    cr.set_source_rgba(*color)
    cr.set_line_join(style.join)
    cr.set_line_cap(style.cap)

    if style.dash:
        cr.set_dash(style.dash, 0)

    lines = style.tool_line(stroke)
    for line in lines:
        cr.set_line_width(line.width)

        if style.brush:
            brush = style.brush[line.pressure]
            cr.set_source(brush)

        draw_line(line, cr, draw_stroke)

    cr.restore()

def draw_line(
        line: rdata.LinePath,
        cr: cairo.Context,
        draw_stroke: tp.Any
    ) -> None:
    """
    Draw line using Cairo context.

    :param line: Line to draw.
    :param cr: Cairo context.
    :param draw_stroke: Drawing stroke function (i.e. line or filled area).
    """
    # on new path, the position of point is undefined and first `line_to`
    # call acts as `move_to`
    cr.new_path()
    for x, y in line.points:
        cr.line_to(x, y)
    draw_stroke()

def draw_fill(cr):
    """
    Draw Cairo shape and fill.
    """
    cr.close_path()
    cr.fill()

@contextmanager
def draw_context(pdf_doc: tp.Optional[Poppler.Document], fn_out: str) \
        -> tp.Generator[rdata.Context, None, None]:
    """
    Create Remt project drawing context.
    """
    # mechanical_pencil = style_default(
    #     tool_line=tool.line_mechanical_pencil,
    #     brush=load_brush_dir('mechanical-pencil'),
    # )
    #
    # marker = style_default(
    #     tool_line=tool.line_marker,
    #     brush=load_brush_dir('marker'),
    # )
    #
    # pencil = style_default(
    #     tool_line=tool.line_pencil,
    #     brush=load_brush_dir('pencil'),
    # )

    styles = defaultdict(lambda: STYLE_UNKNOWN_TOOL, {
        rdata.Pen.BALLPOINT_1: style_default(tool_line=tool.line_ballpoint),
        rdata.Pen.BALLPOINT_2: style_default(tool_line=tool.line_ballpoint),

        rdata.Pen.FINELINER_1: style_default(tool_line=tool.line_fineliner),
        rdata.Pen.FINELINER_2: style_default(tool_line=tool.line_fineliner),

        rdata.Pen.PAINTBRUSH_1: style_default(tool_line=tool.line_paintbrush),
        rdata.Pen.PAINTBRUSH_2: style_default(tool_line=tool.line_paintbrush),

        rdata.Pen.MARKER_1: style_default(tool_line=tool.line_marker),
        rdata.Pen.MARKER_2: style_default(tool_line=tool.line_marker),

        rdata.Pen.HIGHLIGHTER_1: STYLE_HIGHLIGHTER,
        rdata.Pen.HIGHLIGHTER_2: STYLE_HIGHLIGHTER,

        rdata.Pen.CALIGRAPHY: style_default(tool_line=tool.line_caligraphy),

        # rdata.Pen.PENCIL_1: pencil,
        # rdata.Pen.PENCIL_2: pencil,
        # rdata.Pen.MECHANICAL_PENCIL_1: mechanical_pencil,
        # rdata.Pen.MECHANICAL_PENCIL_2: mechanical_pencil,

        rdata.Pen.ERASER: STYLE_ERASER,
        rdata.Pen.ERASER_AREA: STYLE_ERASER._replace(
            tool_line=tool.line_erase_area
        ),
    })

    surface = cairo.PDFSurface(fn_out, const.PAGE_WIDTH, const.PAGE_HEIGHT)
    try:
        cr_ctx = cairo.Context(surface)
        yield rdata.Context(
            surface,
            cr_ctx,
            pdf_doc,
            styles,
            itertools.count(),
        )
    finally:
        surface.finish()

def load_brush_dir(fn: str) -> rdata.BrushPatterns:
    replace_null = lambda prev, v: v if v[1] else (v[0], prev[1])

    brushes = ((i, load_brush(fn, i)) for i in range(100))
    items = accumulate(brushes, replace_null, initial=(None, None))
    items = itz.drop(1, items)
    result = tp.cast(rdata.BrushPatterns, dict(items))
    assert list(result) == list(range(100))
    if any(v is None for v in result.values()):
        raise ValueError('Invalid data for brush: {}'.format(fn))
    return result

def load_brush(fn: str, n: int) -> tp.Optional[cairo.SurfacePattern]:
    try:
        fn_brush = path_brush(fn, '{:02d}.png'.format(n))
        data = pkgutil.get_data('remt', fn_brush)
    except FileNotFoundError:
        return None
    else:
        assert data is not None
        img = cairo.ImageSurface.create_from_png(io.BytesIO(data))
        brush = cairo.SurfacePattern(img)
        brush.set_extend(cairo.EXTEND_REPEAT)
        return brush

# vim: sw=4:et:ai
