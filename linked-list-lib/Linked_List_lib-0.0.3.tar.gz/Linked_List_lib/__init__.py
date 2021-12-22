# -*- coding: utf-8 -*-

# Author: Daniel Yang <daniel.yj.yang@gmail.com>
#
# License: BSD 3-Clause License


from .__about__ import (
    __version__,
    __license__,
)

from .singly_linked_list import sll_node

# this is for "from <package_name> import *"
__all__ = ["sll_node",]
