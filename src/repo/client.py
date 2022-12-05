from typing import Iterable

from pymongo import MongoClient

from src.repo.base import BaseRepo
from src.schemas import Client, ClientCreate, ClientUpdate, Filter


class ClientRepo(BaseRepo[Client, ClientCreate, ClientUpdate]):
    def get_by_filter(
            self,
            db_client: MongoClient,
            filter_: Filter
    ) -> Iterable[Client]:
        db_collection = self.get_db_collection(db_client)
        return map(
            lambda obj: Client(**obj),
            db_collection.find(filter=filter_.dict())
        )


client = ClientRepo(Client, 'api', 'client')
