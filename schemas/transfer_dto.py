from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class TransferDto(BaseModel):
    transferId: str
    fromAccountId: str
    toAccountId: str
    amount: float
    createdAt: str

class PaginatedTransfersResponse(BaseModel):
    content: List[TransferDto]
    totalPages: int
