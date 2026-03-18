from pydantic import BaseModel
from decimal import Decimal

class LoanCreate(BaseModel):
    account_id: int
    amount: Decimal
    term_months: int

class LoanOut(BaseModel):
    loan_id: int
    approve_status: str
