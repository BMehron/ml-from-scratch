"""Build Order: You are given a list of projects and a list of dependencies (which is a list of pairs of
projects, where the second project is dependent on the first project). Ail of a project's dependencies
must be built before the project is. Find a build order that will allow the projects to be built. If there
is no valid build order, return an error."""

from typing import List, Tuple, Optional, Dict
from collections import defaultdict
from ctci_4_0 import TreeNode

class Solution:
    def dfs(self, u: int, status: List[int], graph: Dict, order: List[int]) -> bool:
        status[u] = 1
        for v in graph[u]:
            if status[v] == 1:
                return False
            elif status[v] == 0:
                is_valid = self.dfs(v, status, graph, order)
                if not is_valid:
                    return False

        status[u] = 2
        order.append(u)
        return True

    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        graph = defaultdict(list)
        for (u, v) in prerequisites:
            graph[v].append(u)
        
        order = []
        status = defaultdict(lambda: 0)
        for u in range(numCourses):
            if status[u] == 0:
                is_valid = self.dfs(u, status, graph, order)
                if not is_valid:
                    return []
        return order[::-1]






