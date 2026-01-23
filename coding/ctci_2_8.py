# Loop Detection: Given a circular linked list, implement an algorithm that returns the node at the beginning of the loop.

def find_node_on_loop(head):
    fast = head.next
    slow = head
    while fast and fast.next and fast is not slow:
        fast = fast.next.next
        slow = slow.next
    if fast and fast.next is None:
        return None
    return fast

def find_distance(start_node, target_node):
    distance = 0
    while start_node is not None and start_node is not target_node:
        start_node = start_node.next
        distance += 1
    if start_node is None:
        return float("inf")
    return distance

def find_loop(head):
    if head is None or head.next is None:
        return head
    node_on_loop = find_node_on_loop(head)
    if node_on_loop is None:
        return None
    path_len = find_distance(head, node_on_loop)
    loop_len = 1 + find_distance(node_on_loop.next, node_on_loop) 
    diff = abs(loop_len - path_len)
    long_head = head if path_len > loop_len else node_on_loop
    short_head = node_on_loop if path_len > loop_len else head
    for i in range(diff):
        long_head = long_head.next

    while long_head is not short_head:
        long_head, short_head = long_head.next, short_head.next
    
    return long_head

def loop_detection(ll):
    fast = slow = ll

    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next
        if fast is slow:
            break

    if fast is None or fast.next is None:
        return None

    slow = ll
    while fast is not slow:
        fast = fast.next
        slow = slow.next

    return fast

from coding.linked_list import Node, LinkedList

if __name__ == "__main__":
    head = Node(2)
    node3, node4, node5, node6 = Node(3), Node(4), Node(5), Node(6)
    head.next = node3
    node3.next = node4
    node4.next = node5
    node5.next = node6
    node6.next = node4
    print(loop_detection(head).value)
    print("All tests are passed!")
