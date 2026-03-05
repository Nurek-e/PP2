import re

pattern = r"^ab{2,3}$"

text = input()

if re.match(pattern, text):
    print("Match")
else:
    print("No match")