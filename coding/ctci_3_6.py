class Animal:
    def __init__(self, name: str, order: int):
        self.name = name
        self.order = order
        self.next = None

    def __lt__(self, other):
        if not isinstance(other, Animal):
            return NotImplemented
        return self.order < other.order

class LinkedList:
    def __init__(self, head=None, tail=None):
        self.head = head
        self.tail = tail

    def enqueue(self, node: Animal):
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next, self.tail = node, node

    def dequeue(self):
        if self.head is None:
            raise IndexError("dequeue from empty queue")
        node, self.head = self.head, self.head.next
        if self.head is None:
            self.tail = None
        return node
    
class Shelter:
    def __init__(self):
        self.dogs = LinkedList()
        self.cats = LinkedList()
        self.order = 0

    def enqueue(self, animal_type: str, name: str):
        new_animal = Animal(name, self.order)
        self.order += 1
        if animal_type == "dog":
            self.dogs.enqueue(new_animal)
        elif animal_type == "cat":
            self.cats.enqueue(new_animal)
        else:
            raise ValueError("animal_type must be 'dog' or 'cat'")

    def dequeueDog(self):
        return self.dogs.dequeue()

    def dequeueCat(self):
        return self.cats.dequeue()

    def dequeueAny(self):
        if self.dogs.head is None and self.cats.head is None:
            raise IndexError("dequeueAny from empty shelter")
        if self.dogs.head is None:
            return self.cats.dequeue()
        if self.cats.head is None:
            return self.dogs.dequeue()
        return self.dogs.dequeue() if self.dogs.head < self.cats.head else self.cats.dequeue()


