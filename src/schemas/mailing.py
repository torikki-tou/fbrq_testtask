import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class Filter(BaseModel):
    operator_code: Optional[int] = None
    tag: Optional[str] = None


class MailingBase(BaseModel):
    start_time: datetime.datetime
    message_text: str
    filter: Filter
    end_time: datetime.datetime


class MailingCreate(MailingBase):
    pass


class MailingUpdate(MailingBase):
    pass


class MailingInDBBase(MailingBase):
    id: str = Field(alias='_id')

    @validator('id', pre=True)
    def validate_id(cls, v): return str(v)


class Mailing(MailingInDBBase):
    pass
