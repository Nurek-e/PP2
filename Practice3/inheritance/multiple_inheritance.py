# 1) 
class A:
    def show_a(self):
        print("A")

class B:
    def show_b(self):
        print("B")

class C(A, B):
    pass

c = C()
c.show_a()
c.show_b()


# 2)
class Father:
    def __init__(self):
        self.surname = "Khan"

class Mother:
    def __init__(self):
        self.eye_color = "brown"

class Child(Father, Mother):
    def __init__(self):
        Father.__init__(self)
        Mother.__init__(self)

ch = Child()
print(ch.surname, ch.eye_color)


# 3)
class Fly:
    def fly(self):
        print("Flying")

class Swim:
    def swim(self):
        print("Swimming")

class Duck(Fly, Swim):
    pass

d = Duck()
d.fly()
d.swim()


# 4) 
class A:
    def show(self):
        print("A")

class B:
    def show(self):
        print("B")

class C(A, B):
    pass

obj = C()
obj.show() 