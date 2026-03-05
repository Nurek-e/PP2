import re

pattern = r"^[a-z]+_[a-z]+$"

text = input()

if re.match(pattern, text):
    print("Match")
else:
    print("No match")