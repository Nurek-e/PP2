# 1
class Car:
    brand = "Toyota"
    year = 2020

c1 = Car()
print(c1.brand, c1.year)


# 2)
class Phone:
    model = "iPhone"
    color = "black"

p1 = Phone()
p2 = Phone()
print(p1.model, p1.color)
print(p2.model, p2.color)


# 3)
class Game:
    name = "CS2"

g1 = Game()
g2 = Game()
g1.name = "GTA V"   
print(g1.name)
print(g2.name)


# 4)
class Point:
    x = 0
    y = 0

pt = Point()
pt.x = 5
pt.y = 7
print(pt.x, pt.y)