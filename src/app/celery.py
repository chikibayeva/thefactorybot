import os

from celery import Celery
from kombu import Exchange, Queue


if not ('DJANGO_SETTINGS_MODULE' in os.environ):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('thefactorybot')


app.conf.task_queues = [
    Queue('thefactorybot-celery', Exchange('thefactorybot-celery'), routing_key='thefactorybot-celery')
]

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
