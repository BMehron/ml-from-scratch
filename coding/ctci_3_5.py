#Sort Stack: Write a program to sort a stack such that the smallest items are on the top. 
# You can use an additional temporary stack, but you may not copy the elements into any other data structure (such as an array).
#  The stack supports the following operations: push, pop, peek, and is Empty.


def sort_stack(stack):
    sorted_stack = []
    while stack:
        top = stack.pop()
        while sorted_stack and sorted_stack[-1] < top:
            stack.append(sorted_stack.pop())
        sorted_stack.append(top)
    return sorted_stack

if __name__ == "__main__":
    stack = [4,5,2,3,4,9,1]
    print(sort_stack(stack))