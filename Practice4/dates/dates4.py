from datetime import datetime

date1 = input()
date2 = input()

d1 = datetime.strptime(date1, "%Y-%m-%d %H:%M:%S")
d2 = datetime.strptime(date2, "%Y-%m-%d %H:%M:%S")

diff = d2 - d1

print(int(diff.total_seconds()))
