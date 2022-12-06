from bson import ObjectId
from pymongo import MongoClient

from src.repo.base import BaseRepo
from src.schemas import Message, MessageCreate, MessageUpdate, MessageStatus


class MessageRepo(BaseRepo[Message, MessageCreate, MessageUpdate]):
    def count_by_mailing_and_status(
            self,
            db_client: MongoClient,
            mailing_id: str | ObjectId,
            status: MessageStatus
    ) -> int:
        collection = self.get_db_collection(db_client)
        return collection.count_documents(
            {'mailing_id': str(mailing_id), 'status': status.value}
        )


message = MessageRepo(Message, 'api', 'message')
