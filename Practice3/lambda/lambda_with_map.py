nums = [1, 2, 3, 4, 5]

#1
res1 = list(map(lambda x: x + 10, nums))
print(res1) 

#2
res2 = list(map(lambda x: x * x, nums))
print(res2) 

#3
s = ["10", "20", "30"]
res3 = list(map(lambda x: int(x), s))
print(res3)  

#4
a = [1, 2, 3]
b = [10, 20, 30]
res4 = list(map(lambda x, y: x + y, a, b))
print(res4)