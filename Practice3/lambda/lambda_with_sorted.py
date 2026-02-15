nums = [5, 2, 9, 1, 7]

#1
print(sorted(nums)) 

#2
print(sorted(nums, reverse=True))  

#3
words = ["banana", "kiwi", "apple", "cherry"]
print(sorted(words, key=lambda w: len(w)))  

#4
people = [
    {"name": "Ali", "age": 20},
    {"name": "Dana", "age": 18},
    {"name": "Ramazan", "age": 19}
]
sorted_people = sorted(people, key=lambda p: p["age"])
print(sorted_people)