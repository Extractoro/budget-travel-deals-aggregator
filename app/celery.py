import os

from dotenv import load_dotenv
from celery import Celery

load_dotenv()

celery_app = Celery('aggregator')
celery_app.conf.broker_url = os.getenv("CELERY_BROKER_URL", "redis://redis:6379")
celery_app.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379")

celery_app.autodiscover_tasks(['app.tasks'])
