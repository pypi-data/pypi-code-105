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
PDF utilities.
"""

import gi  # type: ignore
gi.require_version('Poppler', '0.18')  # noqa: E402

import pathlib  # noqa: E402
from gi.repository import Poppler  # type: ignore  # noqa: E402

from . import const  # noqa: E402
from .data import TextSelection, Stroke  # noqa: E402


def pdf_open(fn: str) -> Poppler.Document:
    """
    Open PDF file and return Poppler library PDF document.

    :param fn: PDF file name.
    """
    path = pathlib.Path(fn).resolve().as_uri()
    return Poppler.Document.new_from_file(path)

def pdf_scale(page: Poppler.Page) -> float:
    """
    Get scaling factor for a PDF page to fit reMarkable tablet vector data
    onto the page.

    :param page: Poppler PDF page object.
    """
    w, h = page.get_size()
    return max(w / const.PAGE_WIDTH, h / const.PAGE_HEIGHT)  # type: ignore

def pdf_area(page: Poppler.Page, selection: TextSelection) \
        -> Poppler.Rectangle:
    """
    Get PDF page area for a text selection data.

    :param page: Poppler PDF page object.
    :param selection: Text selection data.
    """
    factor = pdf_scale(page)
    y = selection.y * factor

    area = Poppler.Rectangle()
    area.x1 = selection.x1 * factor
    area.y1 = y - 1
    area.x2 = selection.x2 * factor
    area.y2 = y + 1

    return area

def pdf_text(page: Poppler.Page, selection: TextSelection) -> str:
    """
    Having a reMarkable tablet stroke data, get text annotated by the
    stroke.

    :param page: Poppler PDF page object.
    :param selection: Text selection data.
    """
    area = pdf_area(page, selection)
    return page.get_text_for_area(area)  # type: ignore

def pdf_highlight_text(
        doc: Poppler.Document, page: int, stroke: Stroke
    ) -> None:
    """
    Create highlight text annotation in PDF ddocument.

    :param doc: Poppler PDF document object.
    :param page: Page index.
    :param stroke: reMarkable tablet stroke information.
    """
    pdf_page = doc.get_page(page)
    factor = pdf_scale(pdf_page)
    _, height = pdf_page.get_size()

    p1 = stroke.segments[0]
    p2 = stroke.segments[0]
    area = Poppler.Rectangle()
    y = p1.y * factor
    area.x1 = p1.x * factor
    area.y1 = y - 1
    area.x2 = p2.x * factor
    area.y2 = y + 1

    region = pdf_page.get_selected_region(
        1.0, Poppler.SelectionStyle.GLYPH, area
    )
    quads = []
    for i in range(region.num_rectangles()):
        r = region.get_rectangle(i)
        q = Poppler.Quadrilateral()

        x1, y1 = r.x + r.width, height - r.y - r.height
        x2, y2 = r.x, height - r.y
        q.p1 = poppler_point(x1, y1)
        q.p2 = poppler_point(x2, y1)
        q.p3 = poppler_point(x1, y2)
        q.p4 = poppler_point(x2, y2)
        quads.append(q)

    if quads:
        extents = region.get_extents()
        bbox = Poppler.Rectangle()
        bbox.x1 = extents.x
        bbox.x2 = extents.x + extents.width
        bbox.y1 = height - extents.y
        bbox.y2 = height - extents.y - extents.height

        markup = Poppler.AnnotTextMarkup.new_highlight(doc, bbox, quads)
        color = Poppler.Color()
        color.red = 65500
        color.green = 0
        color.blue = 0
        markup.set_color(color)
        markup.set_label(stroke.text)
        markup.set_opacity(0.2)
        pdf_page.add_annot(markup)

def poppler_point(x: float, y: float) -> Poppler.Point:
    """
    Convert coordinates to Poppler point object.
    """
    p = Poppler.Point()
    p.x = x
    p.y = y
    return p

# vim: sw=4:et:ai
