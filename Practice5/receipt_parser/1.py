import re

pattern = r"^ab*$"

text = input()

if re.match(pattern, text):
    print("Match")
else:
    print("No match")