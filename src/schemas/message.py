import datetime

from pydantic import BaseModel


class MessageBase(BaseModel):
    created_at: datetime.datetime = datetime.datetime.now()
    status: str
    client_id: str
    mailing_id: str


class MessageInDBBase(MessageBase):
    id: str


class Message(MessageBase):
    pass


