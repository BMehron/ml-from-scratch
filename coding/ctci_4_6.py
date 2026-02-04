"""Successor: Write an algorithm to find the "next" node (i.e., in-order successor) of a given node in a
binary search tree. You may assume that each node has a link to its parent."""

from typing import List
from collections import deque
from ctci_4_0 import TreeNode



def find_successor(node: TreeNode):
    if node.right:
        node = node.right
        while node.left:
            node = node.left
        return node

    while node.parent:
        if node.parent.left == node:
            return node.parent
        node = node.parent

    return None


