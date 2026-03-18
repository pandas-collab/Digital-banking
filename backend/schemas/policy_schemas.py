from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PolicyCreate(BaseModel):
    coverage_type: str = Field(..., min_length=1)
    coverage_amount: float = Field(..., gt=0)
    premium_monthly: float = Field(..., gt=0)

class PolicyOut(BaseModel):
    id: int
    coverage_type: str
    coverage_amount: float
    premium_monthly: float
    status: str
    next_premium_date: datetime

    class Config:
        orm_mode = True
