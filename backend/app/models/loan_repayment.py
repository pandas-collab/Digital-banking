from sqlalchemy import Column, String, Date, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
import uuid
from .database import Base

class LoanRepayment(Base):
    __tablename__ = "loan_repayments"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    loan_id = Column(PG_UUID(as_uuid=True), ForeignKey("loans.id"), nullable=False)
    due_date = Column(Date, nullable=False)
    amount = Column(Numeric(14, 2), nullable=False)
    principal = Column(Numeric(14, 2), nullable=False)
    interest = Column(Numeric(14, 2), nullable=False)
    status = Column(String(12), nullable=False, default="DUE")  # DUE, PAID, DEFAULT

    loan = relationship("Loan", back_populates="repayments")
