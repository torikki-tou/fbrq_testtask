from typing import Iterable

from pymongo import MongoClient

from src.repo.base import BaseRepo
from src.schemas import Mailing, MailingCreate, MailingUpdate


class MailingRepo(BaseRepo[Mailing, MailingCreate, MailingUpdate]):
    def get_multi(
            self,
            db_client: MongoClient,
            limit: int = 10,
            offset: int = 0
    ) -> Iterable:
        collection = self.get_db_collection(db_client)
        return map(
            lambda obj: Mailing(**obj),
            collection.find(skip=offset).limit(limit)
        )


mailing = MailingRepo(Mailing, 'api', 'mailing')
