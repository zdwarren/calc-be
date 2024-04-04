import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calc_be.settings')

app = Celery('calc_be')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
