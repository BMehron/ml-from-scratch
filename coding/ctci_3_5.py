class StackWithSortMethod:
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self, default_value = None):
        if len(self.stack) == 0:
            return default_value
        return self.stack.pop()

    def peek(self, default_value=None):
        if len(self.stack) == 0:
            return default_value
        return self.stack[-1]

    def __len__(self):
        return len(self.stack)
    
    def is_empty(self):
        return len(self.stack) == 0
    
    def sort(self):
        if len(self) <= 1:
            return

        half = StackWithSortMethod()
        for _ in range(len(self) // 2):
            half.push(self.pop())

        half.sort()
        self.sort()

        merged = StackWithSortMethod()
        while not half.is_empty() or not self.is_empty():
            a = half.peek(float("inf"))
            b = self.peek(float("inf"))
            if a <= b:
                merged.push(half.pop())
            else:
                merged.push(self.pop())

        # merged has largest on top, reverse so smallest on top
        self.stack = merged.stack[::-1]


class StackWithSortMethod:
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if not self.stack:
            raise IndexError("pop from empty stack")
        return self.stack.pop()

    def peek(self):
        if not self.stack:
            raise IndexError("peek from empty stack")
        return self.stack[-1]

    def __len__(self):
        return len(self.stack)

    def is_empty(self):
        return len(self.stack) == 0

    def sort(self):
        """
        Sort so that the smallest items are on the TOP (end of list).
        Uses only one additional stack. O(n^2) time, O(n) extra space.
        """
        temp = StackWithSortMethod()

        while not self.is_empty():
            x = self.pop()

            # Keep temp in DESCENDING order bottom->top
            # (so its TOP is the smallest).
            while not temp.is_empty() and temp.peek() < x:
                self.push(temp.pop())

            temp.push(x)

        # Move back: after this, self.TOP (end) is the smallest.
        while not temp.is_empty():
            self.push(temp.pop())




import unittest
import random

# import StackWithSortMethod from your module
# from your_module import StackWithSortMethod

class TestSortStack(unittest.TestCase):
    def stack_from_list(self, values):
        """
        Push values in given order.
        Here we treat the END of internal list as the TOP of stack (standard).
        """
        s = StackWithSortMethod()
        for v in values:
            s.push(v)
        return s

    def pop_all(self, s):
        out = []
        while not s.is_empty():
            out.append(s.pop())
        return out

    def test_empty_stack_sort(self):
        s = StackWithSortMethod()
        s.sort()
        self.assertTrue(s.is_empty())
        self.assertEqual(len(s), 0)

    def test_single_element_sort(self):
        s = self.stack_from_list([5])
        s.sort()
        self.assertEqual(s.peek(), 5)
        self.assertEqual(self.pop_all(s), [5])

    def test_already_sorted_smallest_on_top(self):
        # To have smallest on top, the top element should be smallest.
        # If top is the end, pushing [3,2,1] means top=1 (smallest).
        s = self.stack_from_list([3, 2, 1])
        s.sort()
        popped = self.pop_all(s)
        self.assertEqual(popped, [1, 2, 3])  # smallest comes out first

    def test_reverse_sorted(self):
        # Push [1,2,3] => top=3 (largest), sort should make top=1
        s = self.stack_from_list([1, 2, 3])
        s.sort()
        popped = self.pop_all(s)
        self.assertEqual(popped, [1, 2, 3])

    def test_with_duplicates(self):
        s = self.stack_from_list([4, 1, 3, 1, 2, 2])
        s.sort()
        popped = self.pop_all(s)
        self.assertEqual(popped, sorted([4, 1, 3, 1, 2, 2]))

    def test_with_negative_numbers(self):
        s = self.stack_from_list([0, -10, 5, -3, 2])
        s.sort()
        popped = self.pop_all(s)
        self.assertEqual(popped, sorted([0, -10, 5, -3, 2]))

    def test_randomized_property(self):
        # Property-based style: after sorting, popping produces sorted order.
        for _ in range(50):
            vals = [random.randint(-100, 100) for _ in range(random.randint(0, 30))]
            s = self.stack_from_list(vals)
            s.sort()
            popped = self.pop_all(s)
            self.assertEqual(popped, sorted(vals))

    def test_len_preserved(self):
        vals = [5, 1, 4, 2, 3]
        s = self.stack_from_list(vals)
        n = len(s)
        s.sort()
        self.assertEqual(len(s), n)
        self.assertEqual(self.pop_all(s), sorted(vals))

    def test_peek_and_pop_empty_default(self):
        s = StackWithSortMethod()
        self.assertIsNone(s.peek())
        self.assertIsNone(s.pop())
        self.assertEqual(s.pop(123), 123)
        self.assertEqual(s.peek(456), 456)

if __name__ == "__main__":
    unittest.main()


    