a=int(input())
def n(nums):
    for i in range(nums,-1,-1):
        yield i
        

for x in n(a):
    print(x)