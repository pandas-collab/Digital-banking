"""SQLAlchemy model for ledger entries."""

from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import BigInteger, Numeric, Text, TIMESTAMP, VARCHAR
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.database import Base

class Ledger(Base):
    """Immutable ledger entry for cash-flow events."""

    __tablename__ = "ledger"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    event_type: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    transfer_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    from_account_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    to_account_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    amount: Mapped[float] = mapped_column(Numeric(precision=15, scale=2), nullable=False)
    from_balance_before: Mapped[float] = mapped_column(Numeric(precision=15, scale=2), nullable=False)
    from_balance_after: Mapped[float] = mapped_column(Numeric(precision=15, scale=2), nullable=False)
    to_balance_before: Mapped[float] = mapped_column(Numeric(precision=15, scale=2), nullable=False)
    to_balance_after: Mapped[float] = mapped_column(Numeric(precision=15, scale=2), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=func.now(), nullable=False, index=True
    )
    audit_data: Mapped[Dict[str, Any]] = mapped_column(JSONB, default={}, nullable=False)

    @property
    def is_debit(self) -> bool:
        """Check if this is a debit (outflow) from the from_account."""
        return self.from_balance_after < self.from_balance_before

    @property
    def is_credit(self) -> bool:
        """Check if this is a credit (inflow) to the to_account."""
        return self.to_balance_after > self.to_balance_before
