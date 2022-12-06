import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pymongo import MongoClient

from src.mailing.tasks import start_mailing
from src import schemas, repo
from src.api import deps


router = APIRouter()


@router.get(
    '/',
    response_model=List[schemas.MailingStats],
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK
)
def get_all_mailings(
        limit: int = 10,
        offset: int = 0,
        db_client: MongoClient = Depends(deps.mongo_client)
):
    mailings = repo.mailing.get_multi(db_client, limit=limit, offset=offset)
    stats = []
    for mailing in mailings:
        delivered = repo.message.count_by_mailing_and_status(
            db_client,
            mailing_id=mailing.id,
            status=schemas.MessageStatus.DELIVERED
        )
        undelivered = repo.message.count_by_mailing_and_status(
            db_client,
            mailing_id=mailing.id,
            status=schemas.MessageStatus.UNDELIVERED
        )
        failed = repo.message.count_by_mailing_and_status(
            db_client,
            mailing_id=mailing.id,
            status=schemas.MessageStatus.FAILED
        )

        stats.append(schemas.MailingStats(
            mailing_data=mailing,
            messages=schemas.MessagesStats(
                delivered=delivered,
                undelivered=undelivered,
                failed=failed
            )
        ))
    return stats


@router.get(
    '/{mailing_id}',
    response_model=schemas.Mailing,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK
)
def get_mailing(
        mailing_id: str,
        db_client: MongoClient = Depends(deps.mongo_client)
):
    mailing = repo.mailing.get(db_client, id_=mailing_id)
    if not mailing:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return mailing


@router.post(
    '/',
    response_model=schemas.Mailing,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED
)
def create_mailings(
        obj_in: schemas.MailingCreate,
        db_client: MongoClient = Depends(deps.mongo_client)
):
    mailing = repo.mailing.create(db_client, obj_in=obj_in)
    if not mailing.end_time < datetime.datetime.now():
        start_mailing.apply_async(
            args=(mailing.dict(by_alias=True),),
            eta=mailing.start_time,
            expires=mailing.end_time,
            ignore_result=True
        )
    return mailing


@router.patch(
    '/{mailing_id}',
    response_model=schemas.Mailing,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK
)
def update_mailing(
        mailing_id: str,
        obj_in: schemas.MailingCreate,
        db_client: MongoClient = Depends(deps.mongo_client)
):
    mailing = repo.mailing.update(
        db_client, id_=mailing_id, obj_in=obj_in
    )
    if not mailing:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return mailing


@router.delete(
    '/{mailing_id}',
    response_model=schemas.Mailing,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK
)
def delete_mailing(
        mailing_id: str,
        db_client: MongoClient = Depends(deps.mongo_client)
):
    mailing = repo.mailing.remove(db_client, id_=mailing_id)
    if not mailing:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return mailing
