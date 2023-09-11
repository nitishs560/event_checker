from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_checker.settings')

app = Celery('event_checker')
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object(settings, namespace = 'CELERY')

#  Celery beat Settings
"""This setting schedules celery worker to go live(event_email_processor) at a given crontab"""
app.conf.beat_schedule = {
    "send-mail-every-day-at-8":{
        'task': 'event_email.tasks.event_email_processor',
        'schedule': crontab(hour=0, minute=1),
    }
}
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request}')