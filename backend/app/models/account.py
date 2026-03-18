from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime, func
from sqlalchemy.orm import relationship
from . import Base

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    balance = Column(Numeric(10, 2), default=0)
    created_at = Column(DateTime, server_default=func.now())
    user = relationship("User")
