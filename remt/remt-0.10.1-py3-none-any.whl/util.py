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
Remt project utilities.
"""

import typing as tp
from collections.abc import Sequence
from itertools import groupby, chain
from operator import attrgetter
from cytoolz.itertoolz import partition  # type: ignore

T = tp.TypeVar('T')

flatten = chain.from_iterable
to_point_y = attrgetter('y')

def split(
        key: tp.Callable[..., bool],
        seq: Sequence[tp.Any],
    ) -> tp.Iterable[tuple[tp.Any, ...]]:
    """
    Split sequence by a function key.

    :param key: Key function.
    :param seq: Sequence to split.
    """
    items = (tuple(v) for k, v in groupby(seq, key))
    items = partition(2, items)
    items = ((v1[-1], v2) for v1, v2 in items)
    yield from items

# vim: sw=4:et:ai
