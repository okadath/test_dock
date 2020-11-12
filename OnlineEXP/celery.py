# import os
# from celery import Celery
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OnlineEXP.settings')
# app = Celery('mysite')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OnlineEXP.settings')
app = Celery('proj') #Nota 1
app.config_from_object('django.conf:settings', namespace='CELERY') #Nota 2
app.autodiscover_tasks() #Nota 3
# app.conf.update(
#     BROKER_URL = 'amqp://localhost:5672/', #Nota 4
# )