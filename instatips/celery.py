from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'instatips.settings')

app = Celery('instatips')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.beat_schedule = {
    # name of the scheduler

    'get-countries-from-api-once-a-month': {
        # task name which we have created in tasks.py
        'task': 'get_countries_from_api',

        # execute on the first day of each month
        'schedule': crontab(0, 0, day_of_month='1')
    },
    # name of the scheduler

    'get-leagues-from-api-at-midnight': {
        # task name which we have created in tasks.py
        'task': 'get_leagues_from_api',

        # execute each day at midnight
        'schedule': crontab(minute=0, hour=0)
    },
    # name of the scheduler

    "get-today-matches-from-api-every-seventeen-minutes": {
        # task name which we have created in tasks.py
        'task': 'get_today_matches_from_api',

        # execute every two hours
        'schedule': crontab(minute='*/17')
    },
    # name of the scheduler

    "get-live-matches-from-api-every-two-mins": {
        # task name which we have created in tasks.py
        'task': 'get_live_matches_from_api',

        # execute every two mins
        'schedule': crontab(minute='*/2')
    },
    # name of the scheduler

    "get-tomorrow-matches-from-api-at-midnight": {
        # task name which we have created in tasks.py
        'task': 'get_tomorrow_matches_from_api',

        # execute each day at midnight
        'schedule': crontab(minute=0, hour=0)
    },
    # name of the scheduler

    "get-day-after-tomorrow-matches-from-api-at-midnight": {
        # task name which we have created in tasks.py
        'task': 'get_day_after_tomorrow_matches_from_api',

        # execute each day at midnight
        'schedule': crontab(minute=0, hour=0)
    }

}
