from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
import os

app = Flask(__name__)

class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': 'apschedule:msg',
            'args': (),
            'trigger': 'interval',
            'seconds': 30
        }
    ]
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'
    SCHEDULER_API_ENABLED = True

scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))

def msg():
    os.system("ipconfig/all")

    os.system("python line.py")

# @scheduler.task('interval', id='job_2', seconds=30, misfire_grace_time=900)
# def job2():
#     print('Job 2 executed')


if __name__ == '__main__':
    app.config.from_object(Config())
    
    scheduler.init_app(app)
    scheduler.start()
    
    app.run()



