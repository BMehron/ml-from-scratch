from coding.linked_list import Node

# Partition: Write code to partition a linked list around a value x, such that all nodes less than x come before all nodes greater than or equal to x. 
# If x is contained within the list, the values of x only need to be after the elements less than x (see below). The partition element x can appear anywhere in the "right partition"; 
# it does not need to appear between the left and right partitions.


def partition(head, partition_value):
    # Base case: list consistis of <= 1 node: Then we just can leave the list untouched
    if head is None or head.next is None:
        return head 
    # we track 3 nodes.
    cur_head, prev_node, cur_node = head, head, head.next 
    # we iterate through the list
    while cur_node is not None:
        if cur_node.value < partition_value:
            # we remove the node from the middle
            prev_node.next = cur_node.next
            # move the node to the head
            cur_node.next = cur_head
            # update our tracked variables
            cur_head, cur_node = cur_node, prev_node.next
        else:
            prev_node, cur_node = cur_node, cur_node.next
    return cur_head


from coding.linked_list import Node
head = Node(3)
node1 = Node(9)
node2 = Node(4)
node3 = Node(5)
node4 = Node(3)

head.next = node1
node1.next= node2
node2.next = node3
node3.next = node4

if __name__ == "__main__":
    new_head = partition(head, 2)
    while new_head:
        print(new_head.value)
        new_head = new_head.next

