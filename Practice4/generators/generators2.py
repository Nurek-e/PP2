a=int(input())
def n(nums):
    for i in range(nums+1):
        if i%2==0:
            yield i

result=",".join(str(x) for x in n(a))
print(result)