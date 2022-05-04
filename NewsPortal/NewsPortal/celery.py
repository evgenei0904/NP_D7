import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'news_every_week': {
        'task': 'news.tasks.post_week',
        'schedule': crontab(minute='0', hour='8', day_of_week='mon'),
    },
}

