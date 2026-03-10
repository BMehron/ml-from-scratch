
# First Common Ancestor: Design an algorithm and write code to find the first common ancestor
# of two nodes in a binary tree. Avoid storing additional nodes in a data structure. NOTE: This is not
# necessarily a binary search tree.

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def dfs(self, node, p, q, meet_num):
        before = meet_num[0]

        if node in [p, q]:
            meet_num[0] += 1    

        if node.left is not None:
            ancestor = self.dfs(node.left, p, q, meet_num)
            if ancestor is not None:
                return ancestor

        if node.right is not None:
            ancestor = self.dfs(node.right, p, q, meet_num)
            if ancestor is not None:
                return ancestor

        if before == 0 and meet_num[0] == 2:
            return node
        return None


    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        return self.dfs(root, p, q, [0])
        

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def lowestCommonAncestor(self, root, p, q):
        if not root or root == p or root == q:
            return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left and right:
            return root
        return left if left else right
        