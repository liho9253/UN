from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
import os
    
    
    
app = Flask(__name__)

class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': 'apschedule:main',
            'args': (),
            'trigger': 'cron',
            'hour' : '6',
            'minute' : '31'
        }
    ]
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'
    SCHEDULER_API_ENABLED = True

scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))

# def msg():
#     os.system("ipconfig/all")

#     os.system("python line.py")

def main():
    os.system("ipconfig/all")

    os.system("python z2.py")

if __name__ == '__main__':
    app.config.from_object(Config())
    
    scheduler.init_app(app)
    scheduler.start()
    
    app.run()
    
    
    