import datetime
import pytz
from datetime import date
tz=pytz.timezone('America/Phoenix')
def getPreviousYear(curr_month):
    year = int(curr_month / 100)
    return year-1


def subtractDays(curr_day, numberOfDays):
    return (datetime.datetime.strptime(curr_day, '%Y%m%d') - datetime.timedelta(days=numberOfDays)).strftime(
        "%Y%m%d")


def subtractHours(curr_hour, numberOfHours):
    return (datetime.datetime.strptime(curr_hour, '%Y%m%d%H') - datetime.timedelta(hours=numberOfHours)).strftime("%Y%m%d%H")

def subtractWeeks(curr_week, numberOfWeeks):
    return (datetime.datetime.strptime(c + '-1', "%Y%W-%w") - datetime.timedelta(weeks=numberOfWeeks)).strftime(
        "%Y%W")

def getPreviousYear(curr_month):
    year = int(curr_month / 100)
    return year-1
now = datetime.datetime.now()
print(now)
a='2020010101'
b='20200101'
c='202033'
#date=datetime.datetime.strptime(a, '%Y%m%d').strftime('%m/%d/%Y')
#print(subtractHours(a,24))
#print(subtractDays(b,30))
print(subtractWeeks(c,2))
#print((datetime.datetime.strptime(c, '%Y%W')))
print(datetime.datetime.strptime(c, '%Y%W') - datetime.timedelta(weeks=2))

r = datetime.datetime.strptime(str(int(c)-1) + '-1', "%Y%W-%w").strftime('%m-%d')
print(r)

weekNumber = date.today().isocalendar()[1]
print ('Week number:', weekNumber)