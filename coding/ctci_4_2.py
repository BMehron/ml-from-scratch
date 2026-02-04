"""Minimal Tree: Given a sorted (increasing order) array with unique integer elements, write an
algorithm to create a binary search tree with minimal height."""

from typing import List
from collections import deque
from ctci_4_0 import TreeNode

def build_bst(nums: List[int]):
    if not nums:
        return None
    
    mid = len(nums) // 2

    root = TreeNode(nums[mid])
    root.left = build_bst(nums[:mid])
    root.right = build_bst(nums[mid+1:])

    return root

# Time: O(n* (building copy: n)) Space: O(n)

def build_bst(nums: List[int]):
    def convert(left, right):            
        if left > right:
            return

        mid = (left + right) // 2

        node = TreeNode(nums[mid])

        node.left = convert(left, mid - 1)
        node.right = convert(mid + 1, right)

        return node
        
    return convert(0, len(nums) - 1)

# Time: O(n), Spance: O(n)



