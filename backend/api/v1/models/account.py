from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.db.base_class import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_number = Column(String, unique=True, index=True)
    balance = Column(Numeric(15, 2), default=0)
    daily_transfer_limit = Column(Numeric(15, 2), default=50000)  # Default daily limit
    monthly_transfer_limit = Column(Numeric(15, 2), default=500000)  # Default monthly limit
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="accounts")
    from_transactions = relationship("Transaction", foreign_keys="Transaction.from_account_id")
    to_transactions = relationship("Transaction", foreign_keys="Transaction.to_account_id")
