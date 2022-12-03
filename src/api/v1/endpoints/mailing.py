from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient

from src import schemas, repo
from src.api import deps


router = APIRouter()


@router.get('/')
def get_all_mailings():
    ...


@router.get(
    '/{mailing_id}',
    response_model=schemas.Mailing,
    status_code=status.HTTP_200_OK
)
def get_all_mailings(
        mailing_id: str,
        db_client: AsyncIOMotorClient = Depends(deps.get_mongo_client)
):
    ...


@router.post(
    '/',
    response_model=schemas.Mailing,
    status_code=status.HTTP_201_CREATED
)
def get_all_mailings(
        obj_in: schemas.MailingCreate,
        db_client: AsyncIOMotorClient = Depends(deps.get_mongo_client)
):
    ...


@router.patch(
    '/{mailing_id}',
    response_model=schemas.Mailing,
    status_code=status.HTTP_200_OK
)
def get_all_mailings(
        mailing_id: str,
        obj_in: schemas.MailingCreate,
        db_client: AsyncIOMotorClient = Depends(deps.get_mongo_client)
):
    ...


@router.delete(
    '/{mailing_id}',
    response_model=schemas.Mailing,
    status_code=status.HTTP_200_OK
)
def get_all_mailings(
        mailing_id: str,
        db_client: AsyncIOMotorClient = Depends(deps.get_mongo_client)
):
    ...
