from celery import Celery
from celery.utils.log import get_task_logger
from celery import shared_task
from datetime import timedelta

log = get_task_logger(__name__)

CELERY_TIMEZONE = 'UTC'
CELERYBEAT_SCHEDULE = {
    'update-every-10-minutes': {
        'task': 'reports.update',
        'schedule': timedelta(minutes=10),
        'args': [],
    },

    'createstats-tip-every-week': {
        'task': 'reports.create_weekly_stats_tip',
        'schedule': timedelta(days=7),
        'args': [],
    },
}

#todo - daily process to remove attacks older than 14 days

app = Celery('reports.tasks', broker='amqp://guest@localhost//')
app.conf.CELERY_TIMEZONE = CELERY_TIMEZONE
app.conf.CELERYBEAT_SCHEDULE = CELERYBEAT_SCHEDULE


@app.task(name='reports.update')
def update():
    return None


@app.task(name='reports.create_weekly_stats_tip')
def create_weekly_stats():
    return None
