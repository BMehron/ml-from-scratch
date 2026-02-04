"""Minimal Tree: Given a sorted (increasing order) array with unique integer elements, write an
algorithm to create a binary search tree with minimal height."""

from typing import List
from collections import deque
from ctci_4_0 import TreeNode

def level_order_traversal(root: TreeNode):
    if root is None:
        return []

    level_order = [[]]
    que = deque([(root, 0)])

    while que:
        top, level = que.popleft()
        if level == len(level_order):
            level_order.append([])
        level_order[-1].append(top.val)
        if top.left:
            que.append((top.left, level + 1))
        if top.right:
            que.append((top.right, level + 1))
    
    return level_order