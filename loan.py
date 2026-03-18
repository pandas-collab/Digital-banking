from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    principal = Column(Float, nullable=False)
    remaining_principal = Column(Float, nullable=False)
    interest_rate = Column(Float, default=0.12)
    term_months = Column(Integer, nullable=False)
    status = Column(String, default="PENDING")  # PENDING, APPROVED, ACTIVE, COMPLETED, DEFAULT
    created_at = Column(DateTime, default=datetime.utcnow)
    next_payment_date = Column(DateTime)
    completed_at = Column(DateTime)
    defaulted_at = Column(DateTime)
    total_repaid = Column(Float, default=0.0)
