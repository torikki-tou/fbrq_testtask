import datetime
from typing import Optional

from pydantic import BaseModel


class MailingBase(BaseModel):
    start_time: Optional[datetime.datetime] = None
    message_text: Optional[str] = None
    filter: Optional[dict] = None
    end_time: Optional[datetime.datetime] = None


class MailingCreate(MailingBase):
    start_time: datetime.datetime
    message_text: str
    filter: dict
    end_time: datetime.datetime


class MailingUpdate(MailingBase):
    pass


class MailingInDBBase(MailingBase):
    id: str


class Mailing(MailingInDBBase):
    pass
