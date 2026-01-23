# Palindrome: Implement a function to check if a linked list is a palindrome.

def find_mindpoint(head):
    if head is None:
        return head
    fast = head
    slow = head
    while fast is not None and fast.next is not None:
        fast = fast.next.next
        slow = slow.next
    return slow

def reverse_linked_list(head):
    if head is None or head.next is None:
        return head 
    prev_node, cur_node = head, head.next
    head.next = None
    while cur_node:
        next_node, cur_node.next = cur_node.next, prev_node
        prev_node, cur_node = cur_node, next_node
    return prev_node

def is_palindrome(head):
    midpoint = find_mindpoint(head)
    reversed_second_half = reverse_linked_list(midpoint)
    first_half = head
    while reversed_second_half:
        if reversed_second_half.value != first_half.value:
            return False
        reversed_second_half = reversed_second_half.next
        first_half = first_half.next

    return True

from coding.linked_list import Node, LinkedList

if __name__ == "__main__":
    tests = [(LinkedList([]), True), (LinkedList([1,2,4,2,0]), False), (LinkedList([1,2,3,4]), False), (LinkedList([1,2,3,2,1]), True),  (LinkedList([1,2,2,1]), True)]
    for linked_list, answer in tests:
        #print(is_palindrome(linked_list.head))
        assert answer == is_palindrome(linked_list.head), f'Wrong on test {linked_list.head}'
    print("All tests are passed!")
