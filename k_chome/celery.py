from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "k_chome.settings")

app = Celery("k_chome")
app.config_from_object('k_chome.celeryconfig', namespace='CELERY')

app.autodiscover_tasks()
