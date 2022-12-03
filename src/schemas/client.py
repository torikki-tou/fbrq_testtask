from typing import Optional

from pydantic import BaseModel


class ClientBase(BaseModel):
    phone_number: Optional[int] = None
    operator_code: Optional[int] = None
    tag: Optional[str] = None
    timezone: Optional[int] = None


class ClientCreate(ClientBase):
    phone_number: int
    operator_code: int
    tag: str
    timezone: int


class ClientUpdate(ClientBase):
    pass


class ClientInDBBase(ClientBase):
    id: str


class Client(ClientInDBBase):
    pass
