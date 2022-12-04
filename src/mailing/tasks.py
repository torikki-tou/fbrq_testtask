from src.core.celery import celery


@celery.task()
def mailing():
    return 
