from fastapi import APIRouter, Depends, HTTPException, status
from pymongo import MongoClient

from src import schemas, repo
from src.api import deps


router = APIRouter()


@router.post(
    '/',
    response_model=schemas.Client,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED
)
def create_client(
        obj_in: schemas.ClientCreate,
        db_client: MongoClient = Depends(deps.mongo_client)
):
    client = repo.client.create(db_client, obj_in=obj_in)
    return client


@router.patch(
    '/{client_id}',
    response_model=schemas.Client,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK
)
def update_client(
        client_id: str,
        obj_in: schemas.ClientUpdate,
        db_client: MongoClient = Depends(deps.mongo_client)
):
    client = repo.client.update(db_client, id_=client_id, obj_in=obj_in)
    if not client:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return client


@router.delete(
    '/{client_id}',
    response_model=schemas.Client,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK
)
def delete_client(
        client_id: str,
        db_client: MongoClient = Depends(deps.mongo_client)
):
    client = repo.client.remove(db_client, id_=client_id)
    if not client:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return client
