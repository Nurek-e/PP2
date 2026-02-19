a=int(input())
def n(nums):
    for i in range(nums):
        yield i*i
    
for x in n(a):
    print(x)