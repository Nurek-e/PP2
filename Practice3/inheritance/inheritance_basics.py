# 1)
class Animal:
    def speak(self):
        print("Animal makes sound")

class Dog(Animal):
    pass

d = Dog()
d.speak()


# 2) 
class Animal:
    def eat(self):
        print("Eating...")

class Cat(Animal):
    def meow(self):
        print("Meow")

c = Cat()
c.eat()
c.meow()


# 3) 
class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    pass

s = Student("Ramazan")
print(s.name)


# 4) 
class Vehicle:
    def move(self):
        print("Moving...")

class Bike(Vehicle):
    def ring(self):
        print("Ring ring!")

b = Bike()
b.move()
b.ring()