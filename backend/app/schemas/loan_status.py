from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from uuid import UUID

class LoanStatusResponse(BaseModel):
    loanId: UUID
    balance: float = Field(ge=0)
    nextDueDate: Optional[date] = None
    status: str = Field(pattern="^(ACTIVE|DEFAULT|CLOSED)$")

    class Config:
        json_encoders = {
            date: lambda v: v.isoformat()
        }
