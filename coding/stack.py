# Stack Implementation

# 1. Using List

class Stack:
    def __init__(self):
        self.size = 0
        self.arr = []
    
    def push(self, value):
        self.size += 1
        self.arr.append(value)
    
    def pop(self):
        if self.size:
            self.arr.pop()


class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

class LinkedListStack:
    def __init__(self):
        self.head = None

    def push(self, x):
        node = Node(x)
        node.next = self.head
        self.head = node

    def pop(self):
        if not self.head:
            raise IndexError("empty")
        val = self.head.val
        self.head = self.head.next
        return val
