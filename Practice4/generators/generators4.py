a=int(input())
b=int(input())
def n(nums,num):
    for x in range(a,b+1):
        yield x*x

for i in n(a,b):
    print(i)