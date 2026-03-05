import re

pattern = r"^[A-Z][a-z]+$"

text = input()

if re.match(pattern, text):
    print("Match")
else:
    print("No match")