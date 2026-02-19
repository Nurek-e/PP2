from datetime import datetime,timedelta
d1=datetime.today()
past=d1-timedelta(days=5)
print(past)
