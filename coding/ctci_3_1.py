from __future__ import annotations
from typing import Any, List


class ThreeStacksInOneArray:
    """
    Three stacks sharing one underlying array of values, using a 'next' array
    to simulate pointers + a free-list.

    All ops are O(1).
    """

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be positive")

        self.capacity = capacity
        self.values: List[Any] = [None] * capacity
        self.next: List[int] = list(range(1, capacity)) + [-1]  # free-list links
        self.tops: List[int] = [-1, -1, -1]  # top index for each of the 3 stacks
        self.free: int = 0  # head of free-list

    def push(self, stack_id: int, value: Any) -> None:
        self._check_stack_id(stack_id)
        if self.free == -1:
            raise OverflowError("No space left in the shared array")

        i = self.free                 # take first free slot
        self.free = self.next[i]      # advance free-list

        self.values[i] = value
        self.next[i] = self.tops[stack_id]  # link to previous top
        self.tops[stack_id] = i             # update top

    def pop(self, stack_id: int) -> Any:
        self._check_stack_id(stack_id)
        top_i = self.tops[stack_id]
        if top_i == -1:
            raise IndexError("Pop from empty stack")

        value = self.values[top_i]
        self.values[top_i] = None

        self.tops[stack_id] = self.next[top_i]  # move top down

        self.next[top_i] = self.free  # put this slot back on free-list
        self.free = top_i

        return value

    def peek(self, stack_id: int) -> Any:
        self._check_stack_id(stack_id)
        top_i = self.tops[stack_id]
        if top_i == -1:
            raise IndexError("Peek from empty stack")
        return self.values[top_i]

    def is_empty(self, stack_id: int) -> bool:
        self._check_stack_id(stack_id)
        return self.tops[stack_id] == -1

    def _check_stack_id(self, stack_id: int) -> None:
        if stack_id not in (0, 1, 2):
            raise ValueError("stack_id must be 0, 1, or 2")
        


if __name__ == "__main__":
    stacks = ThreeStacksInOneArray(capacity=10)

    stacks.push(0, "a0")
    stacks.push(1, "b0")
    stacks.push(2, "c0")
    stacks.push(0, "a1")
    stacks.push(1, "b1")

    print(stacks.pop(0))  # a1
    print(stacks.pop(1))  # b1
    print(stacks.pop(2))  # c0
    print(stacks.peek(0)) # a0
