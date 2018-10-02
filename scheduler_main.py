#!/usr/bin/python

import schedule
import time
import os

def job():
    os.system("cd /home/jeevantm89/src/crypto-market-ticker")
    os.system("/usr/bin/python /home/jeevantm89/src/crypto-market-ticker/main.py")

schedule.every().hour.do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)