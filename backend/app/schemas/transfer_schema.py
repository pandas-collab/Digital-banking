from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class TransferCreate(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: Decimal
    description: Optional[str] = None

class TransferOut(BaseModel):
    transfer_id: int
    from_balance: Decimal
    to_balance: Decimal
