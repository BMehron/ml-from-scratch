"""BST Sequences: A binary search tree was created by traversing through an array from left to right
and inserting each element. Given a binary search tree with distinct elements, print all possible
arrays that could have led to this tree."""

from typing import List, Tuple, Optional, Dict
from collections import defaultdict
from ctci_4_0 import TreeNode

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def merge_seqs(self, left_part, i, right_part, j, cur_seq, all_seqs):
        if i == len(left_part) and j == len(right_part):
            all_seqs.append(cur_seq[:])
            return
        
        if i < len(left_part):
            cur_seq.append(left_part[i])
            self.merge_seqs(left_part, i+1, right_part, j, cur_seq, all_seqs)
            cur_seq.pop()
        
        if j < len(right_part):
            cur_seq.append(right_part[j])
            self.merge_seqs(left_part, i, right_part, j+1, cur_seq, all_seqs)
            cur_seq.pop()

    # Time Complexity: O(len(left_part) + len(right_part) choose len(left_part)) < O(2 ** n)
        


    def generateBSTSequences(self, root: TreeNode) -> List[List[int]]:
        if root is None:
            return [[]]
        
        left_seqs = self.generateBSTSequences(root.left)
        right_seqs = self.generateBSTSequences(root.right)

        all_seqs = []
        for left_part in left_seqs:
            for right_part in right_seqs:
                self.merge_seqs(left_part, 0, right_part, 0, [root.val], all_seqs)
            
        return all_seqs





