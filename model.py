from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from db import Base

class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    size = Column(String, nullable=False)
    dangerous = Column(Boolean, default=False)
    sterilized = Column(Boolean, default=False)
    breed = Column(String, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)