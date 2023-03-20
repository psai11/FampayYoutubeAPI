#API_Youtube/celery.py

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "API_Youtube.settings")
app = Celery("API_Youtube")
app.config_from_object("django.conf:settings", namespace= "CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'fetch-video-every-10-secs': {
      'task': 'fetch-videos',
      'schedule': 10,
      'args': (0, )
    },

   #  'add-every-2-seconds': {
   #    'task': 'add_2_numbers',  
   #    'schedule': 10,
   #    'args': (16, 16) 
   #  },

   #  'print-name-every-5-seconds': {  
   #    'task': 'print_msg_with_name',  
   #    'schedule': 5,  
   #    'args': ("DjangoPY", )  
   #  },
}