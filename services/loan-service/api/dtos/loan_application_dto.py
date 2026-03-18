from typing import Dict, Optional
from decimal import Decimal
from domain.models.loan_application import LoanApplication

class LoanApplicationDTO:
    @staticmethod
    def from_model(model: LoanApplication) -> 'LoanApplicationDTO':
        dto = LoanApplicationDTO()
        dto.id = model.id
        dto.user_id = model.user_id
        dto.amount = float(model.amount)
        dto.term_months = model.term_months
        dto.interest_rate = float(model.interest_rate)
        dto.status = model.status
        dto.purpose = model.purpose
        dto.annual_income = float(model.annual_income)
        dto.employment_status = model.employment_status
        dto.credit_score = model.credit_score
        dto.submitted_at = model.submitted_at.isoformat() if model.submitted_at else None
        return dto

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'amount': self.amount,
            'term_months': self.term_months,
            'interest_rate': self.interest_rate,
            'status': self.status,
            'purpose': self.purpose,
            'annual_income': self.annual_income,
            'employment_status': self.employment_status,
            'credit_score': self.credit_score,
            'submitted_at': self.submitted_at
        }

    def __init__(self):
        self.id: Optional[str] = None
        self.user_id: str = ""
        self.amount: float = 0.0
        self.term_months: int = 0
        self.interest_rate: float = 0.0
        self.status: str = ""
        self.purpose: str = ""
        self.annual_income: float = 0.0
        self.employment_status: str = ""
        self.credit_score: Optional[int] = None
        self.submitted_at: Optional[str] = None
