#1
def my_function(fname, lname):
  print(fname + " " + lname)

my_function("Emil", "Refsnes")


#2
def add(a, b):
    print(a + b)

add(3, 7)


#3
def greet(name="Guest"):
    print("Hi,", name)

greet("Ramazan")
greet()


#4
def sum_all(*nums):
    total = 0
    for x in nums:
        total += x
    print(total)

sum_all(1, 2, 3)
sum_all(10, 20, 30, 40)


#5
def show_user(**info):
    print("name =", info.get("name"))
    print("age =", info.get("age"))

show_user(name="Ramazan", age=18)

