import os
from functools import reduce

base_dir = os.path.dirname(__file__)
scores_path = os.path.join(base_dir, "scores")

students = []

files = os.listdir(scores_path)

for file in files:
    if file.endswith(".txt"):
        with open(os.path.join(scores_path, file), "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    name, score = line.split(",")
                    students.append((name, int(score)))

names = [student[0] for student in students]
scores = [student[1] for student in students]

total_students = len(students)
total_score = sum(scores)
average_score = total_score / total_students
highest_score = max(scores)
lowest_score = min(scores)

increased_scores = list(map(lambda x: x + 5, scores))
top_students = list(filter(lambda x: x[1] > 85, students))
product_scores = reduce(lambda a, b: a * b, scores)
numbered_students = list(enumerate(students, start=1))
combined = list(zip(names, scores))
sorted_students = sorted(students, key=lambda x: x[1], reverse=True)

print("All students:")
for student in students:
    print(student)

print("\nTotal students:", total_students)
print("Total score:", total_score)
print("Average score:", average_score)
print("Highest score:", highest_score)
print("Lowest score:", lowest_score)

print("\nScores increased by 5:")
print(increased_scores)

print("\nTop students (>85):")
for name, score in top_students:
    print(name, score)

print("\nProduct of all scores:")
print(product_scores)

print("\nStudents with index numbers:")
for i, (name, score) in numbered_students:
    print(i, name, score)

print("\nCombined names and scores using zip:")
print(combined)

print("\nStudents sorted by score:")
for name, score in sorted_students:
    print(name, score)

report_path = os.path.join(base_dir, "report.txt")

with open(report_path, "w", encoding="utf-8") as f:
    f.write(f"Total students: {total_students}\n")
    f.write(f"Average score: {average_score}\n")
    f.write(f"Highest score: {highest_score}\n")
    f.write(f"Lowest score: {lowest_score}\n\n")
    f.write("Top students:\n")
    for name, score in top_students:
        f.write(f"{name} {score}\n")