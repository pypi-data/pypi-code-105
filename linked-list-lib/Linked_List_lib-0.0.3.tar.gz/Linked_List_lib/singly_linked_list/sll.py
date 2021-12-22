# -*- coding: utf-8 -*-

#  Author: Daniel Yang <daniel.yj.yang@gmail.com>
#
#  License: BSD 3-Clause License

from typing import Optional

class sll_node(object):

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    
    def __repr__(self) -> str:
        return f"node({self.val})"
    
    def __str__(self) -> str:
        """for print(node)"""
        curr = self
        res = curr.__repr__()
        while curr.next:
            curr = curr.next
            res += f" -> {curr.__repr__()}"
        return res

    @property
    def middle(self):
        mid = speed2x = self
        while speed2x and speed2x.next:
            mid = mid.next
            speed2x = speed2x.next.next
        return mid

    @property
    def reversed(self):
        tmp, prev = self, None
        while tmp:
	        tmp.next, prev, tmp = prev, tmp, tmp.next
        return prev

