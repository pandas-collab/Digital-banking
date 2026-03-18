from sqlalchemy import Column, Integer, Numeric, Enum, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db import Base

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(15, 2), nullable=False)
    interest_rate = Column(Numeric(5, 2), nullable=False)
    term_months = Column(Integer, nullable=False)
    status = Column(Enum('PENDING', 'APPROVED', 'DENIED', name='loan_status'), default='PENDING')
    balance_due = Column(Numeric(15, 2), nullable=False)
    monthly_repayment = Column(Numeric(15, 2), nullable=False)
    next_due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    borrower_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)

    account = relationship("Account", back_populates="loans")
