from datetime import datetime
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class CashFlowEvent:
    """Immutable cash-flow event for 100% transparency"""

    def __init__(self, event_type: str, account_id: str, amount: float,
                 previous_balance: float, new_balance: float,
                 metadata: Optional[Dict] = None):
        self.id = f"{datetime.utcnow().isoformat()}_{account_id}"
        self.timestamp = datetime.utcnow()
        self.event_type = event_type  # DEPOSIT, WITHDRAWAL, TRANSFER, LOAN_PAYMENT, PREMIUM_PAYMENT
        self.account_id = account_id
        self.amount = round(float(amount), 2)
        self.previous_balance = round(float(previous_balance), 2)
        self.new_balance = round(float(new_balance), 2)
        self.metadata = metadata or {}

        # Validate critical fields
        if self.amount < 0:
            raise ValueError(f"Invalid negative amount: {amount}")
        if abs(self.new_balance - (self.previous_balance + self.amount)) > 0.01:
            raise ValueError(f"Balance calculation error: {self.previous_balance} + {self.amount} != {self.new_balance}")

        logger.info(f"Created event {self.id}: {event_type} ${amount} for {account_id}")

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'event_type': self.event_type,
            'account_id': self.account_id,
            'amount': self.amount,
            'previous_balance': self.previous_balance,
            'new_balance': self.new_balance,
            'metadata': self.metadata
        }
