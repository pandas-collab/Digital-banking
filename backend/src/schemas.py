from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import Optional
from datetime import datetime
from uuid import UUID

class TransferRequest(BaseModel):
    fromAccount: str
    toAccount: str
    amount: Decimal = Field(..., gt=0, decimal_places=2)

    model_config = ConfigDict(
        json_encoders={
            Decimal: lambda v: float(v)
        }
    )

class TransferResponse(BaseModel):
    id: str
    fromAccount: str
    toAccount: str
    amount: float
    status: str
    createdAt: datetime

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )

class PaginatedTransferResponse(BaseModel):
    data: list[TransferResponse]
    total: int
    page: int
    size: int
