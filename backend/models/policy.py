from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Policy(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    coverage_type = Column(String(50), nullable=False)
    coverage_amount = Column(Numeric(12, 2), nullable=False)
    premium_monthly = Column(Numeric(6, 2), nullable=False)
    status = Column(String(10), default="active")
    next_premium_date = Column(Date, nullable=False)
    balance_due = Column(Numeric(12, 2), default=0.00)

    account = relationship("Account", back_populates="policies")
