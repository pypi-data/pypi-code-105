# -*- coding: utf-8 -*-

# Author: Daniel Yang <daniel.yj.yang@gmail.com>
#
#  License: BSD 3-Clause License

from Linked_List_lib import sll_node

curr = head = sll_node(1)
curr.next = sll_node(2)
curr = curr.next
curr.next = sll_node(3)
curr = curr.next
curr.next = sll_node(4)
curr = curr.next
curr.next = sll_node(5)

print(head)
print(head.middle)
head = head.reversed
print(head)
head = head.reversed
print(head)

