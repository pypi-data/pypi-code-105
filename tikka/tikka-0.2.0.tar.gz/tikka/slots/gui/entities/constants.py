# Copyright 2021 Vincent Texier <vit@free.fr>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import sys

import wx

from tikka.domains.entities.constants import PACKAGE_PATH

# Standalone executable install
if getattr(sys, "frozen", False):
    IMAGES_PATH = PACKAGE_PATH.joinpath("images")
# Python package install
else:
    IMAGES_PATH = PACKAGE_PATH.joinpath("slots/gui/images/assets")

LOGO_IMAGE = ("logo_tikka_01.jpeg", wx.BITMAP_TYPE_JPEG)
SAFE_IMAGE = ("safe_400x400.png", wx.BITMAP_TYPE_PNG)
SAFE_WITH_BACKGROUND_IMAGE = ("safe_with_background.png", wx.BITMAP_TYPE_PNG)
SAFE_WITH_GIRL_IMAGE = ("safe_with_girl_400x400.png", wx.BITMAP_TYPE_PNG)
LOCKED_IMAGE = ("locked_cartoon_400x400.png", wx.BITMAP_TYPE_PNG)
UNLOCKED_IMAGE = ("unlocked_cartoon_400x400.png", wx.BITMAP_TYPE_PNG)
KEYS_IMAGE = ("keys.png", wx.BITMAP_TYPE_PNG)
HARD_DISK_IMAGE = ("hard_disk.png", wx.BITMAP_TYPE_PNG)
ARROW_LEFT_IMAGE = ("arrow_left.png", wx.BITMAP_TYPE_PNG)
ARROW_RIGHT_IMAGE = ("arrow_right.png", wx.BITMAP_TYPE_PNG)
CONFIG_SYMBOL_IMAGE = ("config_symbol.png", wx.BITMAP_TYPE_PNG)
