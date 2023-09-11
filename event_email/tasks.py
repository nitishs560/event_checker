from celery import shared_task
from event_checker.celery import app
from celery import Celery
from celery.schedules import crontab
from .views import find_events
# app = Celery('event_checker')

@shared_task(bind=True)
def demo_func(self):
    for i in range(5):
        print(i)

    return "Done"

@app.task
def event_email_processor():
    find_events()