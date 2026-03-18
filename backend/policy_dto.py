from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PolicyCreateDTO(BaseModel):
    plan: str = Field(..., min_length=3, max_length=50)
    premium: float = Field(..., gt=0)
    coverage: float = Field(..., gt=0)
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    start_date: Optional[str] = None

class PolicyResponseDTO(BaseModel):
    id: str
    plan: str
    premium: float
    coverage: float
    email: str
    created_at: str
    status: str
