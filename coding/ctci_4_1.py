"""Route Between Nodes: Given a directed graph, design an algorithm to find out whether there is a
route between two nodes."""

from typing import List
from collections import deque

def validPath(n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        graph = [[] for _ in range(n)]
        for (u, v) in edges:
            graph[u].append(v)
            graph[v].append(u)

        que = deque([source])
        visited = set([source])

        while que:
            node = que.popleft()
            if node == destination:
                return True
            for next_node in graph[node]:
                if next_node not in visited:
                    que.append(next_node)
                    visited.add(next_node)
        
        return False



