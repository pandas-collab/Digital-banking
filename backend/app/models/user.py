from sqlalchemy import Column, Integer, String, Enum, DateTime, func
from . import Base
import enum

class RoleEnum(str, enum.Enum):
    admin = "admin"
    customer = "customer"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
