from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from services.loan_service import LoanService
from schemas.loan_schemas import LoanCreateRequest, LoanResponse

router = APIRouter(prefix="/api/v1")

@router.post("/loans", response_model=LoanResponse)
def create_loan(request: LoanCreateRequest, account_id: int, db: Session = Depends(get_db)):
    service = LoanService(db)
    loan = service.create_loan(request, account_id)
    return loan

@router.get("/loans/{loan_id}", response_model=LoanResponse)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    service = LoanService(db)
    loan = service.get_loan_by_id(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan
