import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pymongo import MongoClient

from src.mailing.tasks import start_mailing
from src import schemas, repo
from src.api import deps


router = APIRouter()


@router.get('/')
def get_all_mailings():
    ...


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
    mailing = await repo.mailing.create(db_client, obj_in=obj_in)
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
