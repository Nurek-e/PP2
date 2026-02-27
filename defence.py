class Person():
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def introduce(self):
        print("Hello my name is:",self.name,"I'm",self.age,"years old")

class Student(Person):
    def __init__(self,name,age,grade):
        super().__init__(name,age)
        self.grade=grade
    def introduce1(self):
        print("Grade:",self.grade)



class Doctor():
    def __init__(self,hospital,specification):
        self.hospital=hospital
        self.specification=specification
    def introduce(self):
        print("Hi I'm work in:",self.hospital,"I'm",self.specification,"doctor")

name=input()
age=int(input())
grade=int(input())
hospital=input()
specification=input()
P=Student(name,age,grade)
P.introduce()
P.introduce1()
D=Doctor(hospital,specification)
D.introduce()