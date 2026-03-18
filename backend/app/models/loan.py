from sqlalchemy import Column, Integer, ForeignKey, Numeric, Enum, DateTime, func
from sqlalchemy.orm import relationship
from . import Base
import enum

class LoanStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    defaulted = "defaulted"
    paid = "paid"

class Loan(Base):
    __tablename__ = "loans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    principal = Column(Numeric(10, 2))
    annual_rate = Column(Numeric(5, 2))
    status = Column(Enum(LoanStatus), default=LoanStatus.pending)
    term_months = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    user = relationship("User")
