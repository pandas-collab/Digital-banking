import pytest
from decimal import Decimal
from datetime import datetime
from services.loan_application_service import LoanApplicationService
from domain.models.loan_application import LoanApplication

@pytest.fixture
def loan_service():
    return LoanApplicationService()

@pytest.fixture
def sample_application():
    return LoanApplication(
        id="test-123",
        user_id="user-456",
        amount=Decimal('10000.00'),
        term_months=24,
        interest_rate=Decimal('0.075'),
        status="pending",
        purpose="debt_consolidation",
        annual_income=Decimal('60000'),
        employment_status="full_time",
        credit_score=720,
        submitted_at=datetime.utcnow()
    )

def test_create_application_with_valid_data(self, loan_service):
    data = {
        "amount": 5000,
        "term_months": 36,
        "purpose": "home_improvement",
        "annual_income": 75000,
        "employment_status": "full_time"
    }

    result = loan_service.submit_application("user-123", data)

    assert result.amount == Decimal('5000.00')
    assert result.status == "under_review"
    assert result.user_id == "user-123"

def test_validate_invalid_amount(self, loan_service):
    data = {
        "amount": 0,
        "term_months": 24,
        "purpose": "debt_consolidation",
        "annual_income": 60000,
        "employment_status": "full_time"
    }

    with pytest.raises(ValueError, match="Loan amount must be positive"):
        loan_service.submit_application("user-123", data)

def test_validate_invalid_term(self, loan_service):
    data = {
        "amount": 5000,
        "term_months": 6,
        "purpose": "debt_consolidation",
        "annual_income": 60000,
        "employment_status": "full_time"
    }

    with pytest.raises(ValueError, match="Loan term must be between 12 and 360 months"):
        loan_service.submit_application("user-123", data)

def test_calculate_interest_rate_good_credit(self):
    service = LoanApplicationService()
    rate = service._calculate_interest_rate(24, 750)
    assert abs(rate - Decimal('0.058')) < Decimal('0.001')

    rate = service._calculate_interest_rate(36, 750)
    assert abs(rate - Decimal('0.062')) < Decimal('0.001')

def test_calculate_interest_rate_poor_credit(self):
    service = LoanApplicationService()
    rate = service._calculate_interest_rate(24, 500)
    assert abs(rate - Decimal('0.083')) < Decimal('0.001')
