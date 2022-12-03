from typing import TypeVar, Generic, Type, Optional

from bson import ObjectId
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

Model = TypeVar('Model', bound=BaseModel)
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)


class BaseRepo(Generic[Model, CreateSchema, UpdateSchema]):
    def __init__(self, model: Type[Model], database: str, collection: str):
        self.model = model
        self.database = database
        self.collection = collection
    
    def get_db_collection(
            self, db_client: AsyncIOMotorClient
    ) -> AsyncIOMotorCollection:
        return db_client[self.database][self.collection]

    async def get(
            self,
            db_client: AsyncIOMotorClient,
            id_: str | ObjectId
    ) -> Optional[Model]:
        if not isinstance(id_, ObjectId) and not ObjectId.is_valid(id_):
            return None
        collection = self.get_db_collection(db_client)
        obj = await collection.find_one({'_id': ObjectId(id_)})
        if not obj:
            return None
        obj['id'] = str(obj.pop('_id'))
        return self.model(**obj)

    async def create(
            self,
            db_client: AsyncIOMotorClient,
            obj_in: CreateSchema
    ) -> Model:
        collection = self.get_db_collection(db_client)
        obj_id = (await collection.insert_one(obj_in.dict())).inserted_id
        return await self.get(db_client, id_=obj_id)

    async def update(
            self,
            db_client: AsyncIOMotorClient,
            id_: str | ObjectId,
            obj_in: UpdateSchema
    ) -> Optional[Model]:
        if not isinstance(id_, ObjectId) and not ObjectId.is_valid(id_):
            return None
        collection = self.get_db_collection(db_client)
        await collection.update_one(
            {'_id': ObjectId(id_)},
            {'$set': obj_in.dict()}
        )
        return await self.get(db_client, id_=id_)

    async def remove(
            self,
            db_client: AsyncIOMotorClient,
            id_: str | ObjectId
    ) -> Optional[Model]:
        if not isinstance(id_, ObjectId) and not ObjectId.is_valid(id_):
            return None
        collection = self.get_db_collection(db_client)
        obj = await self.get(db_client, id_=id_)
        if not obj:
            return None
        await collection.delete_one({'_id': ObjectId(id_)})
        return self.model(**obj.dict())
