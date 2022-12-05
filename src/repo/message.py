from src.repo.base import BaseRepo
from src.schemas import Message, MessageCreate, MessageUpdate


class MessageRepo(BaseRepo[Message, MessageCreate, MessageUpdate]):
    pass


message = MessageRepo(Message, 'api', 'message')
