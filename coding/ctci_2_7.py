# Intersection; Given two (singly) linked lists, determine if the two lists intersect.
#  Return the inter- secting node. Note that the intersection is defined based on reference, not value. 
# That is, if the kth node of the first linked list is the exact same node (by reference) as the j t h 
# node of the second linked list, then they are intersecting.

def get_length(head):
    length = 0
    while head:
        length += 1
        head = head.next
    return length

def intersection(list1, list2):
    list1_len = get_length(list1)
    list2_len = get_length(list2)
    long_list = list1 if list1_len > list2_len else list2
    short_list = list2 if list1_len > list2_len else list1
    diff = abs(list1_len - list2_len)
    for _ in range(diff):
        long_list = long_list.next
    while long_list and long_list is not short_list:
        long_list, short_list = long_list.next, short_list.next
    return long_list is not None

from coding.linked_list import Node, LinkedList

if __name__ == "__main__":
    list1 = Node(2)
    list2 = Node(3)
    node4, node5, node6 = Node(4), Node(5), Node(6)
    list1.next = node4
    list2.next = node5 
    node4.next = node6
    node5.next = node6
    print(intersection(list1, list2))