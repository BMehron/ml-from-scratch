"""Check Balanced: implement a function to check if a binary tree is balanced. For the purposes of
this question, a balanced tree is defined to be a tree such that the heights of the two subtrees of any
node never differ by more than one."""

from typing import List
from collections import deque
from ctci_4_0 import TreeNode


def find_depth_and_balance(root: TreeNode):
    if root is None:
        return 1
    
    left_depth = find_depth_and_balance(root.left)
    if left_depth == 0:
        return 0
    
    right_depth = find_depth_and_balance(root.right) 
    if right_depth == 0:
        return 0

    if abs(left_depth - right_depth) > 1:
        return 0

    return 1 + max(left_depth, right_depth)   

def check_balace(root: TreeNode):
    return find_depth_and_balance(root) > 0
