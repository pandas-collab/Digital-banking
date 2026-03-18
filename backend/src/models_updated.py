from sqlalchemy import Column, String, Numeric, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from sqlalchemy.orm import relationship

from .database import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    balance = Column(Numeric(15, 2), nullable=False, default=0)

    outgoing_transfers = relationship("Transfer", foreign_keys="Transfer.from_account", back_populates="from_account_rel")
    incoming_transfers = relationship("Transfer", foreign_keys="Transfer.to_account", back_populates="to_account_rel")
