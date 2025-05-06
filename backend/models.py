from sqlalchemy import Column, Integer, String, Float, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    api_key = Column(String, unique=True, index=True)
    budget = Column(Float, default=1000.0)  # e.g. token budget

class Usage(Base):
    __tablename__ = "usage"
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, index=True)
    tokens = Column(Float)
    timestamp = Column(DateTime, server_default=func.now())
