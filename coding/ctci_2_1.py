from coding.linked_list import Node

def remove_duplicates(head: Node):
    if head is None:
        return head
    prev_node = head
    cur_node = head.next
    while cur_node is not None:
        if prev_node.value != cur_node.value:
            prev_node.next = cur_node
            prev_node = cur_node
        cur_node = cur_node.next
    return prev_node


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
    remove_duplicates(head)
    while head:
        print(head.value)
        head = head.next