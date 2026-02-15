# 1)
class Student:
    school = "KBTU"

    def __init__(self, name):
        self.name = name

s1 = Student("Ramazan")
s2 = Student("Ali")
print(s1.name, s1.school)
print(s2.name, s2.school)


# 2)
Student.school = "AITU"
print(s1.school)
print(s2.school)


# 3) 
s1.school = "NIS"   
print(s1.school)    
print(s2.school)    


# 4) 
class User:
    count = 0 

    def __init__(self, name):
        self.name = name
        User.count += 1

u1 = User("A")
u2 = User("B")
u3 = User("C")
print(User.count) 