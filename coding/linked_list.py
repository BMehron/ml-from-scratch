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

class LinkedList:
    # __iter__, __len__, 
    def __init__(self, values=None):
        self.head = None
        self.tail = None
        if values is not None:
            self.add_multiple_values(values)
        
    def __iter__(self):
        cur_node = self.head
        while cur_node:
            yield cur_node 
            cur_node = cur_node.next

    def add(self, value):
        if self.tail is None:
            self.head=self.tail=Node(value)
        else:
            self.tail.next = Node(value)
            self.tail = self.tail.next
        return self.tail
    
    def add_multiple_values(self, values):
        for v in values:
            self.add(v)

    def __str__(self):
        values = [str(node.value) for node in self]
        return ' -> '.join(values)
    
        
