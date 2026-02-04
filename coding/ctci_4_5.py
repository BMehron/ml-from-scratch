"""Validate BST: Implement a function to check if a binary tree is a binary search tree."""

from typing import List
from collections import deque
from ctci_4_0 import TreeNode


def dfs(root: TreeNode, lower_bound: int, upper_bound: int) -> bool:
    if root is None:
        return True
    
    if root.value <= lower_bound or root.value >= upper_bound:
        return False
    
    return dfs(root.left, lower_bound, root.value) and dfs(root, root.value, upper_bound)

def validate_bst(root: TreeNode):
    return dfs(root, float("-inf"), float("inf"))

