a=int(input())
def n(nums):
    for i in range(nums+1):
        if i%3==0 and i%4==0:
            yield i

for x in n(a):
    print(x)