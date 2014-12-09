#This file controls the scheduling of tasks such as posting to hipchat
#and updating the database with new information

import subprocess
from apscheduler.schedulers.background import BackgroundScheduler

import logging
logging.basicConfig()

def main():
    start_scheduler()
    start_webserver()

def start_scheduler(): 
    sched = BackgroundScheduler()

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

def start_webserver():
    subprocess.call(["gunicorn", "onthegrid.wsgi", "--log-file", "-"])

if __name__ == "__main__":
    main()