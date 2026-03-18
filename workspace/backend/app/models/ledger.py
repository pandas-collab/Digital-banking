from sqlalchemy import Column, DateTime, Numeric, String, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.db import Base

class Ledger(Base):
    __tablename__ = "ledger"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ts = Column(DateTime(timezone=True), server_default=func.now())
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    type = Column(String(32), nullable=False)
    amount = Column(Numeric(14, 2), nullable=False)
    balance_after = Column(Numeric(14, 2), nullable=False)
    metadata = Column(JSON, default={})
