from pydantic import BaseModel, Field, validator
from typing import Optional
from decimal import Decimal

class TransferRequest(BaseModel):
    from_account_id: int = Field(..., gt=0)
    to_account_id: int = Field(..., gt=0)
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    description: Optional[str] = None

    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        if v.as_tuple().exponent < -2:
            raise ValueError('Maximum 2 decimal places allowed')
        return v

    @validator('from_account_id', 'to_account_id')
    def validate_account_ids(cls, v):
        if v <= 0:
            raise ValueError('Account ID must be positive')
        return v

    @validator('to_account_id')
    def accounts_must_be_different(cls, v, values):
        if 'from_account_id' in values and v == values['from_account_id']:
            raise ValueError('From and to accounts must be different')
        return v

class TransactionResponse(BaseModel):
    id: int
    from_account_id: int
    to_account_id: int
    amount: Decimal
    status: str
    transaction_type: str
    description: Optional[str]
    created_at: str

    class Config:
        orm_mode = True

class TransactionHistory(BaseModel):
    transactions: list[TransactionResponse]
    total_count: int
    current_page: int
    total_pages: int

class DailyLimitStatus(BaseModel):
    account_id: int
    daily_limit: Decimal
    used_today: Decimal
    remaining_today: Decimal
    is_limit_exceeded: bool

class MonthlyLimitStatus(BaseModel):
    account_id: int
    monthly_limit: Decimal
    used_this_month: Decimal
    remaining_this_month: Decimal
    is_limit_exceeded: bool
