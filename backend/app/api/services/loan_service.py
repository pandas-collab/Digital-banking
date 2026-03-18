from sqlalchemy.orm import Session
from app.models.loan import Loan, Payment
from app.models.user import User
from app.api.schemas.loan import LoanCreate, PaymentCreate
import uuid
from datetime import datetime, timedelta

def create_loan_number():
    return f"LN-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"

def calculate_monthly_payment(principal: float, annual_rate: float, months: int) -> float:
    """Calculate monthly payment using standard loan formula"""
    if annual_rate == 0:
        return principal / months

    monthly_rate = annual_rate / 100 / 12
    payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
    return round(payment, 2)

def create_loan(db: Session, loan_data: LoanCreate, user_id: int) -> Loan:
    loan_number = loan_data.loan_number or create_loan_number()
    monthly_payment = calculate_monthly_payment(
        loan_data.principal_amount,
        loan_data.interest_rate,
        loan_data.term_months
    )

    loan = Loan(
        user_id=user_id,
        loan_number=loan_number,
        principal_amount=loan_data.principal_amount,
        interest_rate=loan_data.interest_rate,
        term_months=loan_data.term_months,
        monthly_payment=monthly_payment,
        remaining_balance=loan_data.principal_amount,
        next_payment_date=datetime.now() + timedelta(days=30)
    )

    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan

def get_user_loans(db: Session, user_id: int):
    return db.query(Loan).filter(Loan.user_id == user_id).all()

def get_loan_by_id(db: Session, loan_id: int, user_id: int):
    return db.query(Loan).filter(
        Loan.id == loan_id,
        Loan.user_id == user_id
    ).first()

def process_payment(db: Session, loan_id: int, payment_data: PaymentCreate, user_id: int):
    loan = get_loan_by_id(db, loan_id, user_id)
    if not loan:
        return None

    # Calculate interest and principal portions
    daily_rate = loan.interest_rate / 100 / 365
    days_since_payment = 30  # Simplified: assume monthly
    interest_owed = loan.remaining_balance * daily_rate * days_since_payment

    if payment_data.amount <= interest_owed:
        return None  # Payment too low

    principal_paid = payment_data.amount - interest_owed
    new_balance = max(0, loan.remaining_balance - principal_paid)

    payment = Payment(
        loan_id=loan_id,
        amount=payment_data.amount,
        principal_paid=round(principal_paid, 2),
        interest_paid=round(interest_owed, 2),
        payment_method=payment_data.payment_method
    )

    loan.remaining_balance = new_balance
    loan.last_payment_date = datetime.now()

    if new_balance <= 0:
        loan.status = "paid"
        loan.next_payment_date = None
    else:
        loan.next_payment_date = datetime.now() + timedelta(days=30)

    db.add(payment)
    db.commit()
    db.refresh(payment)
    db.refresh(loan)

    return payment, loan
