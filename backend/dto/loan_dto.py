from dataclasses import dataclass
from datetime import datetime

@dataclass
class LoanLedgerItem:
    loan_id: int
    amount: float
    direction: str
    created_at: datetime

@dataclass
class DefaulterAlert:
    loan_id: int
    account_id: int
    missed_amount: float
    alert_time: datetime
