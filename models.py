from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Client(Base):

    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, unique=True, index=True)
    ip_address = Column(String)
    last_seen = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    operating_system = Column(String)


class Command(Base):

    __tablename__ = 'commands'

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    command = Column(String)
    execution = Column(Boolean, default=False)
    execution_time = Column(DateTime)
    result = Column(Text) 

class Admin(Base):

    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)