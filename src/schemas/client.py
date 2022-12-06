from typing import Optional

from pydantic import BaseModel, Field, validator


class ClientBase(BaseModel):
    phone_number: Optional[int] = None
    operator_code: Optional[int] = None
    tag: Optional[str] = None
    timezone: Optional[int] = None


class ClientCreate(ClientBase):
    phone_number: int
    operator_code: int
    timezone: int


class ClientUpdate(ClientBase):
    pass


class ClientInDBBase(ClientBase):
    id: str = Field(alias='_id')

    @validator('id', pre=True)
    def validate_id(cls, v): return str(v)


class Client(ClientInDBBase):
    pass
