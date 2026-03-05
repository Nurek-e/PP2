import re

text = input()

result = re.sub(r"_([a-z])", lambda x: x.group(1).upper(), text)

print(result)