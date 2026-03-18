import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base
from app.models.loan import Loan
from app.api.services.loan_service import create_loan, calculate_monthly_payment

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    yield session
    session.close()

def test_calculate_monthly_payment():
    payment = calculate_monthly_payment(10000, 5, 12)
    assert abs(payment - 856.07) < 0.01

def test_create_loan(db_session):
    from app.models.user import User
    user = User(email="test@example.com", username="test", hashed_password="hashed")
    db_session.add(user)
    db_session.commit()

    from app.api.schemas.loan import LoanCreate
    loan_data = LoanCreate(principal_amount=10000, interest_rate=5, term_months=12)
    loan = create_loan(db_session, loan_data, user.id)

    assert loan.principal_amount == 10000
    assert loan.monthly_payment > 0
    assert loan.remaining_balance == 10000
