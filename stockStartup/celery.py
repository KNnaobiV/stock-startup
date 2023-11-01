import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stockStartup.settings")
app = Celery("stockStartup")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()