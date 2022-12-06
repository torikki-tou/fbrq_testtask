import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, validator


class MessageStatus(str, Enum):
    DELIVERED = 'delivered'
    UNDELIVERED = 'undelivered'
    FAILED = 'failed'


class MessageBase(BaseModel):
    created_at: datetime.datetime = datetime.datetime.now()
    status: MessageStatus = MessageStatus.UNDELIVERED
    client_id: Optional[str] = None
    mailing_id: Optional[str] = None


class MessageCreate(MessageBase):
    client_id: str
    mailing_id: str


class MessageUpdate(MessageBase):
    pass


class MessageInDBBase(MessageBase):
    id: str = Field(alias='_id')

    @validator('id', pre=True)
    def validate_id(cls, v): return str(v)


class Message(MessageInDBBase):
    pass
