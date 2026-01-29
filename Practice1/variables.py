#1
x = "awesome"

def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)
#2
x = 5
y = "John"
print(type(x))
print(type(y))


#3
x, y, z = "Orange", "Banana", "Cherry"

print(x)
print(y)
print(z)

#4
x = "Python "
y = "is "
z = "awesome"
print(x + y + z)

#5
x = "awesome"

def myfunc():
  x = "fantastic"
  print("Python is " + x)

myfunc()

print("Python is " + x)