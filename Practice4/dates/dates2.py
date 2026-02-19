from datetime import datetime,timedelta
d1=datetime.today()
past=d1-timedelta(days=1)
tom=d1+timedelta(days=1)
print(d1)
print(past)
print(tom)
