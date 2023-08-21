import schedule
import time
import os

def projekty():
    os.system("python projekty.py")
    print("Projekty.py run")


schedule.every(10).minutes.do(projekty)

while True:
    schedule.run_pending()
    time.sleep(1)
    print("Waiting")
