from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.api.schemas.loan import LoanCreate, LoanResponse, PaymentCreate, PaymentResponse
from app.api.services import loan_service
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=LoanResponse)
async def create_loan(
    loan: LoanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return loan_service.create_loan(db, loan, current_user.id)

@router.get("/", response_model=List[LoanResponse])
async def get_user_loans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return loan_service.get_user_loans(db, current_user.id)

@router.get("/{loan_id}", response_model=LoanResponse)
async def get_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    loan = loan_service.get_loan_by_id(db, loan_id, current_user.id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan

@router.post("/{loan_id}/payments", response_model=PaymentResponse)
async def make_payment(
    loan_id: int,
    payment: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = loan_service.process_payment(db, loan_id, payment, current_user.id)
    if not result:
        raise HTTPException(status_code=400, detail="Payment processing failed")

    payment_record, loan = result
    return payment_record

@router.get("/{loan_id}/payments")
async def get_payments(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.models.loan import Payment
    loan = loan_service.get_loan_by_id(db, loan_id, current_user.id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    return db.query(Payment).filter(Payment.loan_id == loan_id).all()
