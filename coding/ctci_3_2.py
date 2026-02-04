class StackWithMin:
    def __init__(self):
        self.values = []
        self.mins = []

    def push(self, value):
        self.values.append(value)
        if not self.mins or value <= self.mins[-1]:
            self.mins.append(value)

    def pop(self):
        if not self.values:
            raise IndexError("pop from empty stack")
        value = self.values.pop()
        if value == self.mins[-1]:
            self.mins.pop()
        return value

    def min(self):
        if not self.mins:
            raise IndexError("min from empty stack")
        return self.mins[-1]

    def peek(self):
        if not self.values:
            raise IndexError("peek from empty stack")
        return self.values[-1]

    def __len__(self):
        return len(self.values)
