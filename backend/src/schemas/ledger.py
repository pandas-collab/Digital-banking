"""Pydantic schemas for ledger entries."""

from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, validator

from src.models.ledger import Ledger

class LedgerCreate(BaseModel):
    """Schema for creating a ledger entry (immutable - no updates)."""

    event_type: str = Field(..., regex=r'^(transfer_initiated|transfer_completed|transfer_failed)$')
    transfer_id: int = Field(..., gt=0)
    from_account_id: int = Field(..., gt=0)
    to_account_id: int = Field(..., gt=0)
    amount: Decimal = Field(..., ge=0, decimal_places=2)
    from_balance_before: Decimal = Field(..., decimal_places=2)
    from_balance_after: Decimal = Field(..., decimal_places=2)
    to_balance_before: Decimal = Field(..., decimal_places=2)
    to_balance_after: Decimal = Field(..., decimal_places=2)
    description: Optional[str] = None
    audit_data: Dict[str, Any] = Field(default_factory=dict)

    @validator('audit_data')
    def validate_audit_data(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure audit_data contains expected keys."""
        if not isinstance(v, dict):
            raise ValueError('audit_data must be a dictionary')

        # Optional validation for common audit fields
        if v:
            if 'request_id' in v and not isinstance(v['request_id'], str):
                raise ValueError('request_id must be a string')
            if 'user_agent' in v and not isinstance(v['user_agent'], str):
                raise ValueError('user_agent must be a string')
            if 'ip_address' in v and not isinstance(v['ip_address'], str):
                raise ValueError('ip_address must be a string')

        return v

class LedgerEntry(BaseModel):
    """Schema for ledger entry response."""

    id: int
    event_type: str
    transfer_id: int
    from_account_id: int
    to_account_id: int
    amount: Decimal
    from_balance_before: Decimal
    from_balance_after: Decimal
    to_balance_before: Decimal
    to_balance_after: Decimal
    description: Optional[str]
    created_at: datetime
    audit_data: Dict[str, Any]

    class Config:
        """Pydantic config."""
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }

class LedgerPage(BaseModel):
    """Schema for paginated ledger response."""

    items: list[LedgerEntry]
    total: int
    page: int
    per_page: int

    class Config:
        """Pydantic config."""
        orm_mode = True
