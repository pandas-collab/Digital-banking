from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LoanCreateRequest(BaseModel):
    amount: float
    interest_rate: float
    term_months: int

class LoanResponse(BaseModel):
    id: int
    amount: float
    interestRate: float
    termMonths: int
    status: str
    balanceDue: float
    monthlyRepayment: float
    nextDueDate: Optional[datetime] = None
    createdAt: datetime

    class Config:
        orm_mode = True
        alias_generator = lambda s: ''.join(word.capitalize() if i else word for i, word in enumerate(s.split('_')))
        allow_population_by_field_name = True
