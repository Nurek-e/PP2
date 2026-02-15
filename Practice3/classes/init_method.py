# 1)
class Person:
    def __init__(self, name):
        self.name = name

p = Person("Ramazan")
print(p.name)


# 2)
class Rectangle:
    def __init__(self, w, h):
        self.w = w
        self.h = h

r = Rectangle(3, 4)
print(r.w, r.h)


# 3)
class Student:
    def __init__(self, name, grade=1):
        self.name = name
        self.grade = grade

s1 = Student("Ali")
s2 = Student("Dana", 2)
print(s1.name, s1.grade)
print(s2.name, s2.grade)


# 4)
class Circle:
    def __init__(self, r):
        self.r = r
        self.area = 3.14159 * r * r

c = Circle(5)
print(c.r, c.area)