from typing import Optional, List

class TreeNode:
    def __init__(self, value: Optional[int] = None, left = None, right = None, parent = None):
        self.val = value
        self.left = left
        self.right = right
        self.parent = parent


def in_order_traversal(root: TreeNode):
    if root:
        in_order_traversal(root.left)
        print(root.val)
        in_order_traversal(root.right)

def pre_order_traversal(root: TreeNode):
    if root:
        print(root.val)
        pre_order_traversal(root.left)
        pre_order_traversal(root.right)

def pos_order_traversal(root: TreeNode):
    if root:
        pre_order_traversal(root.left)
        pre_order_traversal(root.right)
        print(root.val)