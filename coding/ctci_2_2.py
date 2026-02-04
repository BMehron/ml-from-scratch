#from coding.linked_list import Node

class Node:
    def __init__(self, value, next=None, prev=None):
        self.value = value
        self.next = next
        self.prev = prev

    def __iter__(self):
        cur_node = self
        while cur_node:
            yield cur_node
            cur_node = cur_node.next

    def __str__(self):
        values = [str(x.value) for x in self]
        return ' -> '.join(values)

def find_kth_to_last(head: Node, k: int):
    assert k > 0, "k should be positive integer."
    fast = head
    while k > 0 and fast is not None:
        fast = fast.next
        k -= 1
    if k > 0 and fast is None:
        return None
    slow = head
    while fast is not None:
        slow, fast = slow.next, fast.next
    return slow
    

import unittest

class Test(unittest.TestCase):
    head = Node(3)
    node1 = Node(7)
    node2 = Node(5)
    node3 = Node(8)
    node4 = Node(3)

    head.next = node1
    node1.next= node2
    node2.next = node3
    node3.next = node4

    test_cases = [
        (head, 1, node4),
        (head, 2, node3),
        (head, 3, node2),
        (head, 4, node1),
        (head, 5, head)
    ]

    def test_function(self):
        for head, k, answer in self.test_cases:
            assert find_kth_to_last(head, k) == answer, f"{find_kth_to_last(head, k)}, {answer}"

if __name__ == "__main__":
    unittest.main()