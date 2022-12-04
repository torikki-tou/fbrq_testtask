from celery import Celery

from src.core.settings import settings


celery = Celery(broker=settings.CELERY_BROKER_CON_STRING)
