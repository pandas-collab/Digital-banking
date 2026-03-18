from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import Optional

class LoanApplication(BaseModel):
    principal_amount: float
    term_months: int

class LoanStatus(BaseModel):
    id: int
    principal: float
    remaining_principal: float
    status: str
    created_at: datetime
    next_payment_date: Optional[datetime]

class LoanRepayment(BaseModel):
    loan_id: int
    amount: float
