import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core', backend='rpc://',
             broker='amqp://myuser:mypassword@localhost:5672/myvhost',
             include=('shop.tasks'))


app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')     # noqa:T201

app.conf.beat_schedule = {
    'shelf_check': {
        'task': 'shop.tasks.shelf_check',
        'schedule': crontab(minute='*/5', hour="*"),
    },
    'check_order_status': {
        'task': 'shop.tasks.check_order_status',
        'schedule': crontab(minute='*/5', hour="*"),
    }
}