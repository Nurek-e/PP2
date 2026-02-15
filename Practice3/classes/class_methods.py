# 1)
class Person:
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print("Hello,", self.name)

p = Person("Ramazan")
p.say_hello()


# 2)
class Calculator:
    def add(self, a, b):
        return a + b

calc = Calculator()
print(calc.add(10, 5))


# 3)
class Counter:
    def __init__(self):
        self.value = 0

    def inc(self):
        self.value += 1

cnt = Counter()
cnt.inc()
cnt.inc()
print(cnt.value)


# 4)
class Rectangle:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def perimeter(self):
        return 2 * (self.w + self.h)

r = Rectangle(3, 7)
print(r.perimeter())