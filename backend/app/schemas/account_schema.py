from pydantic import BaseModel
from decimal import Decimal

class AccountCreate(BaseModel):
    user_id: int

class AccountOut(BaseModel):
    id: int
    user_id: int
    balance: Decimal
    class Config:
        orm_mode = True
