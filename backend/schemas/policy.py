from pydantic import BaseModel
from decimal import Decimal
from datetime import date

class PolicyCreate(BaseModel):
    coverage_type: str
    coverage_amount: float
    premium_monthly: float

class PolicyResponse(BaseModel):
    policy_id: int
    status: str
    premium_monthly: float

class PolicyDetail(BaseModel):
    id: int
    coverage_type: str
    coverage_amount: float
    premium_monthly: float
    status: str
    next_premium_date: date
    balance_due: float

    class Config:
        from_attributes = True
