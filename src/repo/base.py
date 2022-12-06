from typing import TypeVar, Generic, Type, Optional

from bson import ObjectId
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.collection import Collection

Model = TypeVar('Model', bound=BaseModel)
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)


class BaseRepo(Generic[Model, CreateSchema, UpdateSchema]):
    def __init__(self, model: Type[Model], database: str, collection: str):
        self.model = model
        self.database = database
        self.collection = collection
    
    def get_db_collection(
            self, db_client: MongoClient
    ) -> Collection:
        return db_client[self.database][self.collection]

    def get(
            self,
            db_client: MongoClient,
            id_: str | ObjectId
    ) -> Optional[Model]:
        if not isinstance(id_, ObjectId) and not ObjectId.is_valid(id_):
            return None
        collection = self.get_db_collection(db_client)
        obj: Model = collection.find_one({'_id': ObjectId(id_)})
        if not obj:
            return None
        return self.model(**obj)

    def create(
            self,
            db_client: MongoClient,
            obj_in: CreateSchema
    ) -> Model:
        collection = self.get_db_collection(db_client)
        obj_id = (collection.insert_one(obj_in.dict())).inserted_id
        return self.get(db_client, id_=obj_id)

    def update(
            self,
            db_client: MongoClient,
            id_: str | ObjectId,
            obj_in: UpdateSchema
    ) -> Optional[Model]:
        if not isinstance(id_, ObjectId) and not ObjectId.is_valid(id_):
            return None
        collection = self.get_db_collection(db_client)
        collection.update_one(
            {'_id': ObjectId(id_)},
            {'$set': obj_in.dict(exclude_unset=True)}
        )
        return self.get(db_client, id_=id_)

    def remove(
            self,
            db_client: MongoClient,
            id_: str | ObjectId
    ) -> Optional[Model]:
        if not isinstance(id_, ObjectId) and not ObjectId.is_valid(id_):
            return None
        collection = self.get_db_collection(db_client)
        obj = self.get(db_client, id_=id_)
        if not obj:
            return None
        collection.delete_one({'_id': ObjectId(id_)})
        return self.model(**obj.dict())
