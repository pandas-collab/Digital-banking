from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from datetime import datetime

class LoanRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Loan amount must be positive")
    termMonths: int = Field(..., ge=6, le=60, description="Term must be 6-60 months")

class LoanResponse(BaseModel):
    id: str
    userId: str
    amount: float
    termMonths: int
    status: str  # "PENDING"|"APPROVED"|"REJECTED"|"DISBURSED"|"CLOSED"
    approvedAt: Optional[str] = None
    createdAt: Optional[str] = None

class LoanInDB(BaseModel):
    id: UUID
    user_id: UUID
    amount: float
    term_months: int
    status: str
    approved_at: Optional[datetime]
    created_at: datetime
