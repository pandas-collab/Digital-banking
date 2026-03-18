from typing import NamedTuple
from datetime import datetime

class PolicyDTO(NamedTuple):
    id: int
    account_id: int
    coverage_type: str
    coverage_amount: float
    premium_monthly: float
    status: str
    next_premium_date: datetime
    balance_due: float = 0.0  # placeholder if needed
