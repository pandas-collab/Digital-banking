from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Dict, Any, Optional
from uuid import UUID
import re

class LedgerEventResponse(BaseModel):
    id: UUID
    ts: str = Field(..., alias="ts")
    account: UUID = Field(..., alias="account_id")
    type: str
    amount: float
    meta: Dict[str, Any] = Field(..., alias="metadata")

    class Config:
        from_attributes = True

class LedgerQueryParams(BaseModel):
    fromDate: Optional[str] = None
    toDate: Optional[str] = None
    account: Optional[str] = None
    type: Optional[str] = None
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)

    @validator('fromDate', 'toDate')
    def validate_date_format(cls, v):
        if v is None:
            return v
        from dateutil import parser
        try:
            parser.parse(v)
            return v
        except ValueError:
            raise ValueError('Invalid ISO-8601 date format')

    @validator('account')
    def validate_uuid(cls, v):
        if v is None:
            return v
        try:
            UUID(v)
            return v
        except ValueError:
            raise ValueError('Invalid UUID format')

    @validator('type')
    def validate_type(cls, v):
        valid_types = {"TRANSFER", "LOAN", "PREMIUM", "REPAYMENT"}
        if v is None:
            return v
        if v.upper() not in valid_types:
            raise ValueError('Type must be one of: TRANSFER, LOAN, PREMIUM, REPAYMENT')
        return v.upper()

    @validator('fromDate', 'toDate')
    def validate_date_range(cls, v, values):
        if 'fromDate' in values and v is not None and values['fromDate'] is not None:
            if values['toDate'] is not None and v > values['toDate']:
                raise ValueError('fromDate must be before or equal to toDate')
        return v

class LedgerQueryResponse(BaseModel):
    events: list[LedgerEventResponse]
    total: int
