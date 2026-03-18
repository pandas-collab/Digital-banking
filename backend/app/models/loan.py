from sqlalchemy import (
    Column, 
    Integer, 
    ForeignKey, 
    Numeric, 
    Enum, 
    DateTime, 
    String, 
    func
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from . import Base
import enum
import uuid

class LoanStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    defaulted = "defaulted"
    paid = "paid"

class Loan(Base):
    __tablename__ = "loans"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    loan_number = Column(String, unique=True, index=True)
    principal = Column(Numeric(14, 2), nullable=False)
    annual_rate = Column(Numeric(5, 2), nullable=False)
    term_months = Column(Integer, nullable=False)
    monthly_payment = Column(Numeric(14, 2), nullable=False)
    remaining_balance = Column(Numeric(14, 2), nullable=False)
    status = Column(Enum(LoanStatus), default=LoanStatus.pending)
    next_payment_date = Column(DateTime)
    last_payment_date = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user = relationship("User", back_populates="loans")
    payments = relationship("Payment", back_populates="loan", cascade="all, delete-orphan")
    repayments = relationship("LoanRepayment", back_populates="loan")

class LoanRepayment(Base):
    __tablename__ = "loan_repayments"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    loan_id = Column(PG_UUID(as_uuid=True), ForeignKey("loans.id"), nullable=False)
    amount_paid = Column(Numeric(14, 2), nullable=False)
    payment_date = Column(DateTime(timezone=True), server_default=func.now())
    loan = relationship("Loan", back_populates="repayments")

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(PG_UUID(as_uuid=True), ForeignKey("loans.id"), nullable=False)
    amount = Column(Numeric(14, 2), nullable=False)
    principal_paid = Column(Numeric(14, 2), nullable=False)
    interest_paid = Column(Numeric(14, 2), nullable=False)
    payment_date = Column(DateTime, default=func.now())
    payment_method = Column(String)
    loan = relationship("Loan", back_populates="payments")
