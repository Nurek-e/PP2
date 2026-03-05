import json

#Есть 2 файла json instructures и там 4 преподавателя с названием и курсом потом stodents там 8 студентов name:название course:курс потом их прочитаем и на питона заливаем отправляем и потом в питон файле для каждого преподавателя ищем своего студента по курсу и в конце result json выводит преподавателя с названием и курсом и внизу его студенты

instroctors=[{"name":"Nurbek","course":"1"},
            {"name":"Dauren","course":"2"},
            {"name":"Bekzhan","course":"3"},
            {"name":"Nurasyl","course":"4"}]

students=[{"name":"Nurali","course":"1"},
          {"name":"Nurdaulet","course":"1"},
          {"name":"Abutalib","course":"2"},
          {"name":"Almaz","course":"2"},
          {"name":"Nurkhat","course":"3"},
          {"name":"Arnur","course":"3"},
          {"name":"Sake","course":"4"},
          {"name":"Omar","course":"4"}]


result=[]
for teacher in instroctors:
    teacher_a=teacher["course"]
    
    teacher_students=[]
    for student in students:
        if student["course"]==teacher_a:
            teacher_students.append(student["name"])

    result.append({
        "name":teacher["name"],
        "course":teacher_a,
        "students":teacher_students
    })

print(json.dumps(result,ensure_ascii=False,indent=2))
with open("result.json","w",encoding="utf-8") as f:
    json.dump(result,f,ensure_ascii=False,indent=2)