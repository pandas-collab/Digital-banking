from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class LoanBase(BaseModel):
    principal_amount: float = Field(..., gt=0)
    interest_rate: float = Field(..., gt=0, le=100)
    term_months: int = Field(..., gt=0)

class LoanCreate(LoanBase):
    loan_number: Optional[str] = None

class LoanUpdate(BaseModel):
    status: Optional[str] = None
    remaining_balance: Optional[float] = None

class LoanResponse(LoanBase):
    id: int
    loan_number: str
    monthly_payment: float
    remaining_balance: float
    next_payment_date: Optional[datetime]
    last_payment_date: Optional[datetime]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class PaymentBase(BaseModel):
    amount: float = Field(..., gt=0)

class PaymentCreate(PaymentBase):
    payment_method: Optional[str] = None

class PaymentResponse(PaymentBase):
    id: int
    loan_id: int
    principal_paid: float
    interest_paid: float
    payment_date: datetime

    class Config:
        from_attributes = True
