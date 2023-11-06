from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lms.settings")

# Create a Celery instance
app = Celery("lms")

# Load task modules from all registered Django app configs
app.config_from_object("django.conf:settings", namespace="CELERY")

# Autodiscover tasks in all installed apps
app.autodiscover_tasks()


@app.task(bind=True)
def send_email(self, subject, message, from_email, recipient_list):
    from django.core.mail import send_mail

    send_mail(subject, message, from_email, recipient_list)
