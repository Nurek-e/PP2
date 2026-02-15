#1
def sign(x):
    if x > 0:
        return "positive"
    elif x < 0:
        return "negative"
    else:
        return "zero"

print(sign(5))
print(sign(-2))
print(sign(0))


#2
def print_numbers(n):
    for i in range(1, n + 1):
        print(i, end=" ")
    print()

print_numbers(5)


#3
def countdown(n):
    while n > 0:
        print(n, end=" ")
        n -= 1
    print("GO!")

countdown(5)


#4
def first_multiple_of_7(nums):
    for x in nums:
        if x % 7 == 0:
            return x
    return None

print(first_multiple_of_7([3, 10, 14, 20]))
print(first_multiple_of_7([1, 2, 3]))
