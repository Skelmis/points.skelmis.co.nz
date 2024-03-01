import arrow
from arrow import Arrow

now = arrow.now()
past = arrow.now().shift(months=-13)
print("Older then a year", (past - now).days < 365)
