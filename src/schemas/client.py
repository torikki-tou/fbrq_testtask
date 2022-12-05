from typing import Optional

from pydantic import BaseModel, Field, validator


class ClientBase(BaseModel):
    phone_number: int
    operator_code: int
    tag: Optional[str] = None
    timezone: int


class ClientCreate(ClientBase):
    pass


class ClientUpdate(ClientBase):
    pass


class ClientInDBBase(ClientBase):
    id: str = Field(alias='_id')

    @validator('id', pre=True)
    def validate_id(cls, v): return str(v)


class Client(ClientInDBBase):
    pass
