import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email = Column(String, index=True, unique=True)
    name = Column(String)
    hashed_password = Column(String)
    is_admin = Column(Boolean)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
