from datetime import datetime

from sqlalchemy import (ForeignKey,
                        Column, Integer, String, DateTime, BINARY, Boolean)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

BaseModel = declarative_base()


class ClientModel(BaseModel):
    """Table with clients"""
    __tablename__ = 'client'

    id = Column(Integer(), primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    password = Column(BINARY(), nullable=False)
    info = Column(String(255), default='')
    online_status = Column(Boolean(), default='')


class HistoryModel(BaseModel):
    """Table with story inputs clients"""
    __tablename__ = 'history'

    id = Column(Integer(), primary_key=True)
    datetime = Column(DateTime(), default=datetime.now(), nullable=False)
    ip_addr = Column(String(15))
    client_id = Column(Integer(), ForeignKey('client.id'))

    client = relationship('Client',
                          backref=backref('history', order_by=client_id))
