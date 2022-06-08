from __future__ import absolute_import

import os
import sys

from celery import Celery
from django.conf import settings
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'History_of_coins.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Local')

django.setup()

app = Celery('History_of_coins')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
