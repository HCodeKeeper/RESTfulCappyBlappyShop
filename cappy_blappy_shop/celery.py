import os
from celery import Celery
from .settings import config

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cappy_blappy_shop.settings')

celery_app = Celery('cappy_blappy_shop',
                    backend=config.get("CONFIG_BACKEND"),
                    broker=config.get("CELERY_BROKER")
                    )

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
celery_app.autodiscover_tasks()