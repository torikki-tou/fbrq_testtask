import time

import requests

from src import repo, schemas
from src.core.settings import settings
from src.db.mongo import get_mongo_client
from src.core.celery import celery


@celery.task()
def start_mailing(raw_mailing: dict):
    mailing = schemas.Mailing(**raw_mailing)
    clients = repo.client.get_by_filter(
        get_mongo_client(), filter_=mailing.filter
    )

    for client in clients:
        message = repo.message.create(
            get_mongo_client(),
            schemas.MessageCreate(
                client_id=client.id,
                mailing_id=mailing.id
            )
        )
        _send_message.apply_async(
            args=(message.dict(by_alias=True),),
            expires=mailing.end_time,
            ignore_result=True
        )


@celery.task()
def _send_message(raw_message: dict):
    message = schemas.Message(**raw_message)

    try:
        response = requests.post(
            f'https://probe.fbrq.cloud/v1/send/{message.id}',
            headers={'Authorization': settings.PROBE_SERVICE_JWT})
        if response.status_code == 200:
            repo.message.update(
                get_mongo_client(),
                schemas.MessageUpdate(status=schemas.MessageStatus.DELIVERED)
            )
        else:
            repo.message.update(
                get_mongo_client(),
                message.id,
                schemas.MessageUpdate(status=schemas.MessageStatus.FAILED)
            )
    except ConnectionError:
        repo.message.update(
            get_mongo_client(),
            message.id,
            schemas.MessageUpdate(status=schemas.MessageStatus.FAILED)
        )
