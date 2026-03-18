from sqlalchemy import Column, Integer, String, Numeric, Float, Date, DateTime, JSON, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from db import Base as DatabaseBase

Base = declarative_base()

class Policy(Base):
    __tablename__ = "policies"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    policy_number = Column(String, unique=True, nullable=False)
    product_code = Column(String, nullable=False)
    coverage_type = Column(String(50), nullable=False)
    coverage_amount = Column(Float, nullable=False)
    premium = Column(Float, nullable=False)
    premium_monthly = Column(Numeric(6, 2), nullable=False)
    deductible = Column(Float, default=0)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    next_premium_date = Column(Date, nullable=False)
    status = Column(String(10), default="active")
    metadata = Column(JSON)
    balance_due = Column(Numeric(12, 2), default=0.00)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    account = relationship("Account", back_populates="policies")
