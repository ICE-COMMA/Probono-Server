from __future__ import absolute_import, unicode_literals
from datetime import timedelta
from celery import Celery
from django.conf import settings

app = Celery('probono_app')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

CELERY_BEAT_SCHEDULE = {
    'update-api-data': {
        'task': 'probono_app.tasks.get_subway_elvtr_task',
        'schedule': timedelta(days=1),
    },

    
    
    'update-special-weather': {
        'task': 'probono_app.tasks.update_special_weather_task',
        'schedule': timedelta(minutes=30),
    },
}

app.conf.beat_schedule = CELERY_BEAT_SCHEDULE