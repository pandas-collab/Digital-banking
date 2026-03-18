import uuid
from sqlalchemy import Column, String, Numeric, DateTime, Index
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class Transfer(Base):
    __tablename__ = "transfers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    from_account_id = Column(UUID(as_uuid=True), nullable=False)
    to_account_id = Column(UUID(as_uuid=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index('idx_transfers_user_created', user_id, created_at.desc()),
    )
