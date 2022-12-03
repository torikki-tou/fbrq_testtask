from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient

from src import schemas, repo
from src.api import deps


router = APIRouter()


@router.get('/')
async def get_all_mailings():
    ...


@router.get(
    '/{mailing_id}',
    response_model=schemas.Mailing,
    status_code=status.HTTP_200_OK
)
async def get_mailing(
        mailing_id: str,
        db_client: AsyncIOMotorClient = Depends(deps.get_mongo_client)
):
    mailing = await repo.mailing.get(db_client, id_=mailing_id)
    if not mailing:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return mailing


@router.post(
    '/',
    response_model=schemas.Mailing,
    status_code=status.HTTP_201_CREATED
)
async def create_mailings(
        obj_in: schemas.MailingCreate,
        db_client: AsyncIOMotorClient = Depends(deps.get_mongo_client)
):
    mailing = await repo.mailing.create(db_client, obj_in=obj_in)
    return mailing


@router.patch(
    '/{mailing_id}',
    response_model=schemas.Mailing,
    status_code=status.HTTP_200_OK
)
async def update_mailing(
        mailing_id: str,
        obj_in: schemas.MailingCreate,
        db_client: AsyncIOMotorClient = Depends(deps.get_mongo_client)
):
    mailing = await repo.mailing.update(
        db_client, id_=mailing_id, obj_in=obj_in
    )
    if not mailing:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return mailing


@router.delete(
    '/{mailing_id}',
    response_model=schemas.Mailing,
    status_code=status.HTTP_200_OK
)
async def delete_mailing(
        mailing_id: str,
        db_client: AsyncIOMotorClient = Depends(deps.get_mongo_client)
):
    mailing = await repo.mailing.remove(db_client, id_=mailing_id)
    if not mailing:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return mailing
