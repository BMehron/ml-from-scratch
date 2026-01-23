# Sum Lists: You have two numbers represented by a linked list, where each node contains a single digit.
#  The digits are stored in reverse order, such that the Vs digit is at the head of the list. 
# Write a function that adds the two numbers and returns the sum as a linked list.
from coding.linked_list import Node

def get_value(node):
    return node.value if node is not None else 0 

def get_next_node(node):
    return node.next if node is not None else None 

def sum_two_numbers(number_1, number_2):
    # Check if both numbers are None:
    if number_1 is None and number_2 is None:
        return None
    
    result = Node(0)
    memory = 0
    cur_digit = result
    while number_1 is not None or number_2 is not None:
        sum_of_digits = get_value(number_1) + get_value(number_2) + memory
        cur_digit.value = sum_of_digits % 10
        memory = sum_of_digits // 10
        
        number_1 = get_next_node(number_1)
        number_2 = get_next_node(number_2)
        if number_1 is not None or number_2 is not None or memory > 0:
            cur_digit.next = Node(memory)
            cur_digit = cur_digit.next
    
    return result

def reverse_linked_list(head):
    if head is None or head.next is None:
        return head 
    prev_node, cur_node = head, head.next
    head.next = None
    while cur_node:
        next_node, cur_node.next = cur_node.next, prev_node
        prev_node, cur_node = cur_node, next_node
    return prev_node

def sum_two_numbers_folloup(number_1, number_2):
    number_1 = reverse_linked_list(number_1)
    number_2 = reverse_linked_list(number_2)
    print(number_1, number_2)
    return reverse_linked_list(sum_two_numbers(number_1, number_2))

from coding.linked_list import Node, LinkedList

if __name__ == "__main__":
    number_1 = LinkedList([7,1,6])
    number_2 = LinkedList([5,9,2])
    sum = sum_two_numbers_folloup(number_1.head, number_2.head)
    while sum:
        print(sum.value)
        sum = sum.next
