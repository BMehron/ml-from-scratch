import math
import sys

class Animal:
    """General class for animals."""

    def __init__(self, name):
        self.name = name
    
    def speak(self):
        print("Generic animal sound")

class Dog:
    """A simple dog class."""

    def __init__(self, name: str, breed: str):
        self.name = name
        self.breed = breed

    def bark(self):
        print("Woof!!")

    def display_info(self):
        print(f"Name {self.name}")
        print(f"Breed {self.breed}")

class Cat(Animal):
    def __init__(self, name: str, breed: str):
        super().__init__(name)
        self.breed = breed

    def speak(self):
        print("Meow")

class Employee:
    def __init__(self, name: str, salary: int):
        self.name = name
        self._salary = salary

        if self._salary < 1000:
            raise ValueError("Salary is too low!!")

    def get_salary(self):
        try:
            return self._salary / 1
        except:
            print("Something went wrong;")
        finally:
            print("Good Jobs")

        return self._salary
    
    def __all_salaries(self):
        return self._salary

def calculate_area(radius: float) -> float:
    """""
        Calculates the area of a circle
    """
    area = math.pi * radius * radius
    perimeter = 2 * math.pi * radius if radius > 20 else 10
    print(f"Area: {area}", f"Fake perimeter: {perimeter}")
    some_list = [1,2,3,4,5,6]
    even_nums = [x for x in some_list if x % 2 == 0]
    odd_nums = [x for x in some_list if x % 2 == 1]
    print(even_nums, odd_nums)
    not_tuple = ()
    print(not_tuple)
    return area


if __name__ == "__main__":
    # input_radius = float(sys.argv[1])
    # print(f"Calculating the area of a circle given radius: {input_radius}")
    # area = calculate_area(input_radius)
    # print(f"Area: {area}")
    dog = Dog(name="Tyson", breed="Rockeferel")
    cat = Cat(name="Tiny", breed="British")
    cat.speak()
    dog.display_info()
    employee_1 = Employee(name="James", salary=100)
    print(employee_1._salary)
    print(employee_1.get_salary())