from typing import Optional

from pydantic import BaseModel


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
    id: str


class Client(ClientInDBBase):
    pass
