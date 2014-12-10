#This file controls the scheduling of tasks such as posting to hipchat
import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler

import logging
logging.basicConfig()

def main():
    start_scheduler()

def start_scheduler(): 
    sched = BlockingScheduler()

    def db_tasks():
        subprocess.call(["python", "manage.py", "update_vendors"])
        subprocess.call(["python", "manage.py", "update_vendor_events"])

    @sched.scheduled_job('date') #run once immediately on starting the web app
    def scheduled_job():
        db_tasks()

    #Update the database once per day at 10am.
    @sched.scheduled_job('cron', day_of_week='*', hour=10)
    def scheduled_job():
        db_tasks()

    #Post to hipchat wed and fri at 11am
    @sched.scheduled_job('cron', day_of_week='wed,fri', hour=11)
    def scheduled_job():
        subprocess.call(["python", "manage.py", "post_to_hipchat"])

    sched.start()

if __name__ == "__main__":
    main()