from src import repo
from src.db.mongo import get_mongo_client
from src.core.celery import celery
from src.schemas import Mailing, Message, MessageCreate, MessageStatus


@celery.task()
def start_mailing(raw_mailing: dict):
    mailing = Mailing(**raw_mailing)
    clients = repo.client.get_by_filter(
        get_mongo_client(), filter_=mailing.filter
    )

    for client in clients:
        message = repo.message.create(get_mongo_client(), MessageCreate(
            status=MessageStatus.UNDELIVERED,
            client_id=client.id,
            mailing_id=mailing.id
        ))
        _send_message.apply_async(
            args=(message.dict(),),
            expires=mailing.end_time,
            ignore_result=True
        )


@celery.task()
def _send_message(raw_message: dict):
    message = Message.construct(**raw_message)
    print('SENT', message.client_id)
