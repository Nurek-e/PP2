# 1)
class Animal:
    def speak(self):
        print("Animal sound")

class Dog(Animal):
    def speak(self):
        print("Bark")

d = Dog()
d.speak()


# 2) 
class Shape:
    def area(self):
        print("Unknown area")

class Square(Shape):
    def area(self):
        print("Area = side * side")

sq = Square()
sq.area()


# 3)
class A:
    def show(self):
        print("A show")

class B(A):
    def show(self):
        super().show()
        print("B show")

obj = B()
obj.show()


# 4)
class Employee:
    def salary(self):
        return 1000

class Manager(Employee):
    def salary(self):
        return 2000

e = Employee()
m = Manager()
print(e.salary())
print(m.salary())