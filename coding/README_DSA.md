# Data Structures & Algorithms – Practice Exercises

## Introduction

This document contains 20 programming exercises designed to practice core data structures and algorithmic patterns commonly used in technical interviews and real-world software development. Each problem focuses on arrays, strings, and basic data structures, while highlighting a specific algorithmic idea in the solution.

---

## Exercises

### 1. Find Two Numbers That Add Up

**Problem**  
Given an array of integers `nums` and an integer `target`, return the indices of the two numbers such that they add up to `target`.

**Solution**  

```python
from collections import defaultdict
from typing import List, Tuple

def find_all_pairs(nums: List[int], target: int) -> List[Tuple[int, int]]:
    """Return all index pairs (i, j) with i < j and nums[i] + nums[j] == target."""
    seen = defaultdict(list)
    pairs: List[Tuple[int, int]] = []

    for i range(len(nums)):
        for j in seen.get(target - nums[i], []):
            pairs.append((j, i))
        seen[nums[i]].append(i)
    return pairs
```

Time Complexity: O(n + k) = O(n): we iterate over array once plus we iterate over all pairs. Dict Lookup is O(1)

Space Complexity: O(n): we create a dict of value: list[index] from array.

### 2. First Non-Repeating Character

**Problem**
Given a string s, return the index of the first non-repeating character. If none exists, return -1.

**Solution**
```python
from collections import Counter

def find_unique_char_idx(s: str) -> int:
    """ Return index of the first unique char of the string. If none exists, return -1"""
    counter = Counter(s)

    for i, char in enumerate(s):
        if counter[char] == 1:
            return i
    return -1

```
Time Complexity: O(n). Two passes over string

Space Complexity: O(n). We save counter


### 3. Check if a String Is a Palindrome

**Problem**
Determine whether a string is a palindrome, considering only alphanumeric characters and ignoring case.

**Solution**  

```python
def is_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        
        while left < right and not s[right].isalnum():
            right -= 1
        
        if s[left].lower() != s[right].lower():
            return False
        
        left += 1
        right -= 1
    
    return True

```

Time Complexity: O(n). 

Space Complexity: O(1)


### 4. Remove Duplicates from Sorted Array

**Problem**
Given a sorted array, remove duplicates in-place and return the new length.

**Solution**  
```python
from typing import List

def remove_duplicates(nums: List[int]) -> int:
    if not nums:
        return 0

    new_length = 1
    for i in range(1, len(nums)):
        if nums[i] != nums[new_length - 1]:
            nums[new_length] = nums[i]
            new_length += 1

    return new_length
```

Time Complexity: O(n)

Space Complexity: O(1)

### 5. Longest Substring Without Repeating Characters

**Problem**
Find the length of the longest substring without repeating characters.

**Solution**  
```python
def find_longest_unique_substring(s: str) -> int:
    max_length = 0
    start = 0
    unique_chars = set()
    
    for end, char in enumerate(s):
        while char in unique_chars:
            unique_chars.remove(s[start])
            start += 1
        unique_chars.add(char)
        max_length = max(max_length, end-start+1)
    return max_length

def find_longest_unique_substring(s: str) -> int:
    max_length = 0
    start = 0
    seen = {}
    for end, char in enumerate(s):
        start = max(seen.get(char, -1) + 1, start) # instead of while we directly jump
        max_length = max(max_length, end-start+1)
        seen[char] = end
    return max_length
```

Time Complexity: O(n)

Space Complexity: O(n)


### 6. Minimum Length Subarray with Sum at Least Target

**Problem**
Given an array of positive integers and a target sum, find the minimal length of a contiguous subarray whose sum is at least the target.

**Solution**  
```python
from typing import List

def find_min_length(arr: List[int], target: int) -> int:
    if target <= 0:
        return 0

    min_length = float("inf")
    start = 0
    cur_sum = 0

    for end, num in enumerate(arr):
        cur_sum += num
        while cur_sum >= target:
            min_length = min(min_length, end - start + 1)
            cur_sum -= arr[start]
            start += 1
    return min_length if min_length < float("inf") else 0
```
        
Time Complexity: O(n)

Space Complexity: O(1)


### 7. Search Insert Position

**Problem**
Given a sorted array and a target, return the index where the target should be inserted.

**Solution**  
```python
def search_insert_position(arr: List[int], target: int) -> int:
    left, right = -1, len(arr) # arr[left] <= target < arr[right]
    
    while left + 1 < right:
        mid = (left + right) // 2
        
        if target < arr[mid]:
            right = mid
        else:
            left = mid
    
    return left if left >= 0 and arr[left] == target else left + 1
```

Time Complexity: O(nlong)

Space Complexity: O(1)


### 8. Find the First Valid Index

**Problem**
Given a monotonic boolean function ok(i), find the smallest index for which it returns True.

**Solution**  
```python
from typing import Callable

def first_true(ok: Callable[[int], bool]) -> int:
    if ok(0):
        return 0

    right = 1
    while not ok(right):
        right *= 2

    left = right // 2  

    while left + 1 < right:
        mid = (left + right) // 2
        if ok(mid):
            right = mid
        else:
            left = mid
    return right
```

Time Complexity: O(log k) where k is the answer

Space Complexity: O(1)


### 9. Shortest Path in a Grid

**Problem**
Find the shortest path from the top-left to the bottom-right of a grid with blocked cells.

**Solution**  
```python
from collections import deque
from typing import List

def find_shortest_path(grid: List[List[bool]]) -> int:
    if not grid or not grid[0]:
        return -1

    n, m = len(grid), len(grid[0])
    if not grid[0][0] or not grid[n - 1][m - 1]:
        return -1

    distances = [[-1] * m for _ in range(n)]
    distances[0][0] = 0
    que = deque([(0, 0)])

    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while que:
        i, j = que.popleft()
        if i == n - 1 and j == m - 1:
            return distances[i][j]

        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < m and grid[ni][nj] and distances[ni][nj] == -1:
                distances[ni][nj] = distances[i][j] + 1
                que.append((ni, nj))

    return -1

```

Time Complexity: O(nm)

Space Complexity: O(nm)


### 10. Level Order Traversal of a Binary Tree

**Problem**
Return the level-order traversal of a binary tree.

**Solution**  
```python
def level_order_traversal(root):
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
```
Time Complexity: O(n)

Space Complexity: O(n)


### 11. Count Number of Islands

**Problem**
Count the number of connected components of land in a grid.

**Solution**  
```python
from typing import List, Set, Tuple

DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def dfs(i: int, j: int, grid: List[List[bool]], visited: Set[Tuple[int, int]]) -> None:
    visited.add((i, j))
    for di, dj in DIRS:
        ni, nj = i + di, j + dj
        if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]) and (ni, nj) not in visited and grid[ni][nj]:
            dfs(ni, nj, grid, visited)

def num_connected_comps(grid: List[List[bool]]) -> int:
    if not grid or not grid[0]:
        return 0

    visited: Set[Tuple[int, int]] = set()
    num_comps = 0

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] and (i, j) not in visited:
                num_comps += 1
                dfs(i, j, grid, visited)

    return num_comps

```

Time Complexity: O(nm)

Space Complexity: O(nm)


### 12. Check if a Path Exists in a Graph

**Problem**
Given an undirected graph, determine whether a path exists between two nodes.

**Solution**  

```python
from collections import deque

def is_path_exists(graph: List[List[int]], source: int, target: int) -> bool:
    que = deque([source])
    visited = set([source])

    while que:
        node = que.popleft()
        if node == target:
            return True
        for next_node in graph[node]:
            if next_node not in visited:
                que.append(next_node)
                visited.add(next_node)
    
    return False
```
Time Complexity: O(n+e): 

Space Complexity: O(n)

### 13. Generate All Subsets

**Problem**
Return all possible subsets of a set of distinct integers.

**Solution**  
```python
def find_all_subsets(arr):
    all_subsets = [[]]
    for num in arr:
        new_subsets = []
        for subset in all_subsets:
            new_subsets.append(subset + [num])
        all_subsets.extend(new_subsets)
    return all_subsets

def backtracking_subsets(arr):
    answer = []

    def backtrack(idx, subset):
        answer.append(subset[:])
        for i in range(idx, len(arr)):
            subset.append(arr[i])
            backtrack(i + 1, subset)
            subset.pop()

    backtrack(0, [])
    return answer

```
Time Complexity: O(n*2\**n). We have 2\**n subsets, appending create copy so O(n) for each append

Space Complexity: O(n*2\**n). We have 2\**n subsets each with avg size O(n)

### 14. Generate All Permutations

**Problem**
Return all permutations of a list of distinct integers.

**Solution**  
```python
def find_all_permutations(nums):
    permutations = [[]]
    for num in nums:
        new_permutations = []
        for permutation in permutations:
            for i in range(len(permutation)+1):
                new_permutations.append(permutation[:i] + [num] + permutation[i:])
        permutations = new_permutations
    return permutations

def find_all_permutations(nums):
    def backtrack(start):
        if start == len(nums):
            permutations.append(nums[:])
        else:
            for i in range(start, len(nums)):
                nums[start], nums[i] = nums[i], nums[start]
                backtrack(start + 1)
                nums[start], nums[i] = nums[i], nums[start]

    permutations = []
    backtrack(0)
    return permutations

```
Time Complexity: O(n*n!)

Space Complexity: O(n*n!)

### 15. Range Sum Query

**Problem**
Preprocess an array to answer range sum queries efficiently.

**Solution**  

# Prefix Sum
```python
from typing import List, Tuple

def fast_range_sum(arr: List[int], ranges: List[Tuple[int, int]]) -> List[int]:
    n = len(arr)
    prefix = [0] * (n + 1)
    for i in range(len(arr)):
        prefix[i + 1] = prefix[i] + arr[i]

    res = []
    for l, r in ranges:
        # assume 0 <= l <= r < n
        res.append(prefix[r + 1] - prefix[l])
    return res
```
Time Complexity: O(n+q)

Space Complexity: O(n)

### 16. Count Subarrays with Sum K

**Problem**
Count the number of subarrays whose sum equals k.

**Solution**  
```python
from collections import defaultdict

def count_subarray_sum_k(nums: List[int], k: int) -> int:
    answer = 0
    sum_frequency = defaultdict(int)
    sum_frequency[0] = 1
    prefix_sum = 0
    for num in nums:
        prefix_sum += num
        target = prefix_sum - k
        answer += sum_frequency[target]
        sum_frequency[prefix_sum] += 1
    return answer
```

Time Complexity: O(n)

Space Complexity: O(n)

### 17. Find the Kth Largest Element

**Problem**
Return the kth largest element in an unsorted array.

**Solution**  
```python
import heapq

def find_kth_largest(nums: List[int], k: int) -> int:
    if k <= 0 or k > len(nums):
        raise IndexError("k should be in range [1; len(nums)]")
        
    topk_nums = nums[:k]
    heapq.heapify(topk_nums)
    for i in range(k, len(nums)):
        if nums[i] > topk_nums[0]:
            heapq.heappushpop(topk_nums, nums[i])
    return topk_nums[0]     
```
Time Complexity: O(n*logk). There are two other algos: sort then chose and QuickSelect

Space Complexity: O(k)

### 18. Merge K Sorted Lists

**Problem**
Merge k sorted lists into one sorted list.

**Solution**  
```python
import heapq

def merge_k_sorted_lists(arrays: List[List[int]]) -> List[int]:
    merged_array = []

    heap = [(arrays[i][0], i, 0) for i in range(len(arrays)) if len(arrays[i])]
    heapq.heapify(heap)

    while heap:
        next_value, array_idx, value_idx = heapq.heappop(heap)
        merged_array.append(next_value)
        value_idx += 1

        if value_idx < len(arrays[array_idx]):
            heapq.heappush(heap, (arrays[array_idx][value_idx], array_idx, value_idx))
    
    return merged_array

def merge_k_sorted_lists(lists: List[Node]) -> Node:
    merged_lists = ListNode()

    heap = [(node.val, i) for i, node in enumerate(lists) if node]
    heapq.heapify(heap)
    cur_node = merged_lists
    while heap:
        _, i = heapq.heappop(heap)
        cur_node.next, cur_node = lists[i], lists[i]
        lists[i] = lists[i].next
        if lists[i]:
            heapq.heappush(heap, (lists[i].val, i))
    
    return merged_lists.next
```

Time Complexity: O(nlogk)

Space Complexity: O(n)

### 19. Running Median of a Data Stream

**Problem**
Design a data structure that supports adding numbers and retrieving the median.

**Solution**  
```python
import heapq

class MedianFinder:

    def __init__(self):
        self.min_heap = [] # save right half
        self.max_heap = [] # save left half 

    def addNum(self, num: int) -> None:
        if not self.min_heap or self.min_heap[0] <= num:
            heapq.heappush(self.min_heap, num)
        else:
            heapq.heappush(self.max_heap, -num)
            
        if len(self.min_heap) > len(self.max_heap) + 1:
            heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))
        elif len(self.max_heap) > len(self.min_heap) + 1:
            heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))

    def findMedian(self) -> float:
        if len(self.min_heap) + len(self.max_heap) == 0:
            raise IndexError("Median from empty array")

        if len(self.min_heap) == len(self.max_heap):
            return (self.min_heap[0] - self.max_heap[0]) / 2
        return self.min_heap[0] len(self.min_heap) == len(self.max_heap) + 1 else self.max_heap[0] 
```

Time Complexity: O(log n)

Space Complexity: O(n)

### 20. Split Array to Minimize the Largest Sum

**Problem**
Split an array into m contiguous subarrays such that the largest subarray sum is minimized.

**Solution**  

We assume that all nums are positive. We can do dynamic programming keeping d[i, j]  = {answer to the problem for arr[:i] and j partitions}. It will take O(m*n**2) and O(m+n). But this solution is not an optimal. Instead of directly finding the split or trying to use dp, ask simpler question. What if we were asked to check whether we can split an array into max k sub-arrays such that the sum of each array is <= X. This is yes/no question which can be asnwered easily just by greedy algorithm. Another good property is if the answer is no for X then it will be no for all Y < X. And if the answer is yes than it's yes for all Y > X. 

```python
def possible_split(nums: List[int], k: int, upper_bound: int) -> bool:
    bucket_count = 1
    cur_sum = 0
    for num in nums:
        if cur_sum + num > upper_bound:
            if num > upper_bound:
                return False
            else:
                cur_sum = 0
                bucket_count += 1
        cur_sum += num
    return bucket_count <= k


def split_array(nums: List[int], k: int) -> int:
    left, right = max(nums)-1, sum(nums)+1 # f(left) = No < f(answer) = f(right) = Yes
    
    while left + 1 < right:
        mid = (left + right) // 2
        if not self.possible_split(nums, k, mid):
            left = mid
        else:
            right = mid
    
    return right
            
```

Time Complexity: O(n*log(Sum))

Space Complexity: O(1)
