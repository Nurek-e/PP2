# 1)
class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, grade):
        super().__init__(name)
        self.grade = grade

s = Student("Ali", 2)
print(s.name, s.grade)


# 2)
class Animal:
    def __init__(self, type):
        self.type = type

class Dog(Animal):
    def __init__(self, type, name):
        super().__init__(type)
        self.name = name

d = Dog("mammal", "Bobik")
print(d.type, d.name)


# 3) 
class A:
    def show(self):
        print("Class A")

class B(A):
    def show(self):
        super().show()
        print("Class B")

b = B()
b.show()


# 4)
class Base:
    def __init__(self):
        print("Base init")

class Child(Base):
    def __init__(self):
        super().__init__()
        print("Child init")

c = Child()