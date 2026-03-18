from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from decimal import Decimal

@dataclass
class LoanApplication:
    id: Optional[str] = None
    user_id: str = ""
    amount: Decimal = Decimal('0.00')
    term_months: int = 0
    interest_rate: Decimal = Decimal('0.00')
    status: str = "pending"
    purpose: str = ""
    annual_income: Decimal = Decimal('0.00')
    employment_status: str = ""
    credit_score: Optional[int] = None
    submitted_at: datetime = None
    reviewed_at: Optional[datetime] = None
    approved_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.submitted_at:
            self.submitted_at = datetime.utcnow()
