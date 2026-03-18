import pytest
from uuid import uuid4
from datetime import date, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch

from app.models.loan import Loan
from app.models.loan_repayment import LoanRepayment
from app.services.loan_service import LoanService

@pytest.fixture
def test_db_session():
    """Create test database session"""
    engine = create_engine("postgresql://test:test@localhost:5432/test_db")
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()

@pytest.fixture
def sample_loan(test_db_session: Session):
    """Create a sample loan for testing"""
    loan = Loan(
        id=uuid4(),
        user_id=uuid4(),
        amount=Decimal('10000.00'),
        term_months=12,
        interest_rate=Decimal('5.00'),
        status="ACTIVE"
    )
    test_db_session.add(loan)
    test_db_session.commit()

    # Create repayments
    for i in range(12):
        repayment = LoanRepayment(
            id=uuid4(),
            loan_id=loan.id,
            due_date=date.today() + timedelta(days=30*(i+1)),
            amount=Decimal('856.07'),
            principal=Decimal('833.33'),
            interest=Decimal('22.74'),
            status="PAID" if i < 3 else "DUE"
        )
        test_db_session.add(repayment)
    test_db_session.commit()
    return loan

def test_calculate_remaining_balance_with_partial_payments(sample_loan, test_db_session):
    """Test balance calculation with partial payments"""
    balance, next_due, status = LoanService.calculate_remaining_balance(test_db_session, sample_loan.id)

    # 3 payments of 833.33 principal = 2500.00 paid
    assert balance == pytest.approx(7500.00, rel=1e-2)
    assert next_due == date.today() + timedelta(days=30*4)  # 4th payment due
    assert status == "ACTIVE"

def test_loan_not_found(test_db_session):
    """Test handling of non-existent loan"""
    fake_id = uuid4()
    with pytest.raises(ValueError, match="Loan not found"):
        LoanService.calculate_remaining_balance(test_db_session, fake_id)

def test_closed_loan(test_db_session):
    """Test closed loan scenario"""
    loan = Loan(
        id=uuid4(),
        user_id=uuid4(),
        amount=Decimal('1000.00'),
        term_months=1,
        interest_rate=Decimal('0.00'),
        status="CLOSED"
    )
    test_db_session.add(loan)

    # Fully paid repayment
    repayment = LoanRepayment(
        id=uuid4(),
        loan_id=loan.id,
        due_date=date.today(),
        amount=Decimal('1000.00'),
        principal=Decimal('1000.00'),
        interest=Decimal('0.00'),
        status="PAID"
    )
    test_db_session.add(repayment)
    test_db_session.commit()

    balance, next_due, status = LoanService.calculate_remaining_balance(test_db_session, loan.id)

    assert balance == 0.0
    assert next_due is None
    assert status == "CLOSED"

def test_default_loan(test_db_session):
    """Test defaulted loan scenario"""
    loan = Loan(
        id=uuid4(),
        user_id=uuid4(),
        amount=Decimal('5000.00'),
        term_months=6,
        interest_rate=Decimal('5.00'),
        status="ACTIVE"
    )
    test_db_session.add(loan)

    # Create repayments with one defaulted
    repayment1 = LoanRepayment(
        id=uuid4(),
        loan_id=loan.id,
        due_date=date.today() - timedelta(days=30),
        amount=Decimal('856.07'),
        principal=Decimal('833.33'),
        interest=Decimal('22.74'),
        status="PAID"
    )
    repayment2 = LoanRepayment(
        id=uuid4(),
        loan_id=loan.id,
        due_date=date.today() - timedelta(days=60),
        amount=Decimal('856.07'),
        principal=Decimal('833.33'),
        interest=Decimal('22.74'),
        status="DEFAULT"
    )
    test_db_session.add_all([repayment1, repayment2])
    test_db_session.commit()

    balance, next_due, status = LoanService.calculate_remaining_balance(test_db_session, loan.id)

    # Only one payment made = 833.33 paid from 5000.00
    assert balance == pytest.approx(4166.67, rel=1e-2)
    assert status == "DEFAULT"

def test_api_endpoint_success(client, sample_loan):
    """Test API endpoint success case"""
    response = client.get(f"/api/loans/{sample_loan.id}/status")
    assert response.status_code == 200

    data = response.json()
    assert data["loanId"] == str(sample_loan.id)
    assert data["balance"] == pytest.approx(7500.0)
    assert data["status"] == "ACTIVE"
    assert data["nextDueDate"] is not None

def test_api_endpoint_not_found(client):
    """Test API endpoint with invalid ID"""
    fake_id = uuid4()
    response = client.get(f"/api/loans/{fake_id}/status")
    assert response.status_code == 404
    assert response.json()["error"] == "Loan not found"

def test_api_endpoint_invalid_uuid(client):
    """Test API endpoint with invalid UUID format"""
    response = client.get("/api/loans/invalid-uuid/status")
    assert response.status_code == 422
