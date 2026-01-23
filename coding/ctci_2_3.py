# Delete Middle Node: Implement an algorithm to delete a node in the middle (i.e., any node but the first and last node, 
# not necessarily the exact middle) of a singly linked list, given only access to that node.

def delete_middle_node(node):
    node.value = node.next.value
    node.next = node.next.next
    

from coding.linked_list import Node
head = Node(3)
node1 = Node(3)
node2 = Node(5)
node3 = Node(5)
node4 = Node(6)

head.next = node1
node1.next= node2
node2.next = node3
node3.next = node4

if __name__ == "__main__":
    delete_middle_node(node3)
    while head:
        print(head.value)
        head = head.next