from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime
import uuid

class TransferRequest(BaseModel):
    fromAccount: str = Field(..., description="Source account UUID")
    toAccount: str = Field(..., description="Destination account UUID")
    amount: float = Field(..., gt=0, le=100000, description="Transfer amount (max 100,000)")

class TransferResponse(BaseModel):
    id: str
    fromAccount: str
    toAccount: str
    amount: float
    status: Literal["PENDING", "COMPLETED", "FAILED"]
    createdAt: str

    class Config:
        orm_mode = True
