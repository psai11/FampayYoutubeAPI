#API_Youtube/celery.py

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "API_Youtube.settings")
app = Celery("API_Youtube")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()