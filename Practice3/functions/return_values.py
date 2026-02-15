#1
def square(x):
    return x * x

ans = square(6)
print(ans)


#2
def make_full_name(first, last):
    return first + " " + last

print(make_full_name("Daryn", "Abdimanat"))


#3
def min_max(a, b):
    if a < b:
        return a, b
    else:
        return b, a

mn, mx = min_max(9, 2)
print(mn, mx)


#4
def check_positive(x):
    if x <= 0:
        return "NO"
    return "YES"

print(check_positive(-3))
print(check_positive(5))
