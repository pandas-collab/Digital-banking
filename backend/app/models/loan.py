from sqlalchemy import Column, String, Numeric, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
import uuid
from .database import Base

class Loan(Base):
    __tablename__ = "loans"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), nullable=False)
    amount = Column(Numeric(14, 2), nullable=False)
    term_months = Column(Integer, nullable=False)
    interest_rate = Column(Numeric(5, 2), nullable=False)
    status = Column(String(12), nullable=False, default="APPROVED")  # APPROVED, ACTIVE, DEFAULT, CLOSED
    created_at = Column(DateTime, nullable=False, server_default='now()')

    repayments = relationship("LoanRepayment", back_populates="loan")
