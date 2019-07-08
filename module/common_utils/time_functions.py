
import sys
import time
import datetime

# print(sys.path)

def format_to_ymdx():
    nowtime = time.strftime('%Y-%m-%d %X', time.localtime())
    return nowtime

def time_calculate(val):
    date = datetime.date.today() + datetime.timedelta(val)
    return date

def format_to_ymd():
    ymd = time.strftime("%Y-%m-%d")
    return ymd


print(time_calculate(-1))

