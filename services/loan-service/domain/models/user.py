from dataclasses import dataclass
from typing import Optional
from decimal import Decimal

@dataclass
class User:
    id: str = ""
    email: str = ""
    first_name: str = ""
    last_name: str = ""
    date_of_birth: str = ""
    phone: str = ""
    address: str = ""
    annual_income: Decimal = Decimal('0.00')
    employment_status: str = ""
    credit_score: Optional[int] = None
    created_at: str = ""
    updated_at: str = ""
