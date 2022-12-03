from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient

from src import schemas, repo
from src.api import deps


router = APIRouter()


@router.post(
    '/',
    response_model=schemas.Client,
    status_code=status.HTTP_201_CREATED
)
def create_client(
        obj_in: schemas.ClientCreate,
        db_client: AsyncIOMotorClient = Depends(Depends(deps.get_mongo_client))
):
    client = await repo.client.create(db_client, obj_in)
    return client


@router.patch(
    '/{client_id}',
    response_model=schemas.Client,
    status_code=status.HTTP_200_OK
)
def update_client(
        client_id: str,
        obj_in: schemas.ClientUpdate,
        db_client: AsyncIOMotorClient = Depends(deps.get_mongo_client)
):
    client = await repo.client.update(db_client, client_id, obj_in)
    if not client:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return client


@router.delete(
    '/{client_id}',
    response_model=schemas.Client,
    status_code=status.HTTP_200_OK
)
def delete_client(
        client_id: str,
        db_client: AsyncIOMotorClient = Depends(deps.get_mongo_client)
):
    client = await repo.client.remove(db_client, client_id)
    if not client:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return client


