class StackOfPlates:
    def __init__(self, threshold: int):
        if threshold <= 0:
            raise ValueError("threshold must be > 0")
        self.threshold = threshold
        self.stacks = [[]]

    def push(self, value):
        if len(self.stacks[-1]) == self.threshold:
            self.stacks.append([])
        self.stacks[-1].append(value)

    def pop(self):
        if len(self) == 0:
            raise IndexError("pop from empty stack")
        value = self.stacks[-1].pop()
        if len(self.stacks[-1]) == 0 and len(self.stacks) > 1:
            self.stacks.pop()
        return value

    def peek(self):
        if len(self) == 0:
            raise IndexError("peek from empty stack")
        return self.stacks[-1][-1]

    def __len__(self):
        return self.threshold * (len(self.stacks) - 1) + len(self.stacks[-1])
