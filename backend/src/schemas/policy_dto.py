from pydantic import BaseModel, Field, validator
from uuid import UUID
from decimal import Decimal
from typing import Optional

class PolicyCreateRequest(BaseModel):
    planName: str = Field(..., min_length=1, max_length=100)
    premiumAmount: float = Field(..., gt=0)
    coverageAmount: float = Field(..., gt=0)

    @validator('premiumAmount')
    def check_premium_limit(cls, v, values):
        if 'coverageAmount' in values and v > values['coverageAmount'] * 0.05:
            raise ValueError('Premium amount exceeds 5% of coverage amount')
        return v

class PolicyCreateResponse(BaseModel):
    policyId: str

class PolicyDetail(BaseModel):
    id: UUID
    userId: UUID
    planName: str
    premiumAmount: Decimal
    coverageAmount: Decimal
    status: str
    createdAt: str

    class Config:
        from_attributes = True
