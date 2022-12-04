import datetime
from typing import Optional

from pydantic import BaseModel


class MailingBase(BaseModel):
    start_time: datetime.datetime
    message_text: str
    filter: Optional[dict] = None
    end_time: datetime.datetime


class MailingCreate(MailingBase):
    pass


class MailingUpdate(MailingBase):
    pass


class MailingInDBBase(MailingBase):
    id: str


class Mailing(MailingInDBBase):
    pass
