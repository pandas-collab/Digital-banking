from sqlalchemy import Column, String, Numeric, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Policy(Base):
    __tablename__ = "policies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    plan_name = Column(String(100), nullable=False)
    premium_amount = Column(Numeric(10, 2), nullable=False, server_default='0.00')
    coverage_amount = Column(Numeric(12, 2), nullable=False, server_default='0.00')
    status = Column(Enum('active', 'cancelled', 'expired', name='policy_status'), default='active', nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="policies")

    __table_args__ = (
        {'extend_existing': True}
    )
