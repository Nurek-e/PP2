nums = [1, -2, 3, -4, 0, 5, -6]

#1
pos = list(filter(lambda x: x > 0, nums))
print(pos) 

#2
neg = list(filter(lambda x: x < 0, nums))
print(neg)  

#3
even = list(filter(lambda x: x % 2 == 0, nums))
print(even) 

#4
words = ["cat", "python", "hi", "almaty", "code"]
long_words = list(filter(lambda w: len(w) >= 5, words))
print(long_words)