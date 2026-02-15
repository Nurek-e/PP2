#1
add10 = lambda x: x + 10
print(add10(5))

#2
mult = lambda a, b: a * b
print(mult(3, 4))

#3
def make_multiplier(n):
    return lambda x: x * n

times3 = make_multiplier(3)
print(times3(7))

#4
is_even = lambda x: x % 2 == 0
print(is_even(10))  # True
print(is_even(7)) 