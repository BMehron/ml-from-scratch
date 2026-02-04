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

def remove_duplicates(head: Node):
    if head is None:
        return None
    
    while head:
        prev_node, cur_node = head, head.next
        while cur_node:
            if head.value == cur_node.value:
                prev_node.next = cur_node.next
            else:
                prev_node = cur_node
            cur_node = cur_node.next
        head = head.next


head = Node(3)
node1 = Node(3)
node2 = Node(5)
node3 = Node(5)
node4 = Node(3)

head.next = node1
node1.next= node2
node2.next = node3
node3.next = node4

if __name__ == "__main__":
    remove_duplicates(head)
    while head:
        print(head.value)
        head = head.next