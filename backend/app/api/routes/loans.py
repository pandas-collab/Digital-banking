from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session
from uuid import UUID
import logging
from typing import Optional, List
from app.schemas.loan_status import LoanStatusResponse
from app.services.loan_service import LoanService
from app.dependencies import get_db
from app.api.schemas.loan import LoanCreate, LoanResponse, PaymentCreate, PaymentResponse
from app.api.services import loan_service as loan_service_new
from app.core.security import get_current_user
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/loans", tags=["loans"])

@router.post("", response_model=LoanResponse)
async def create_loan(
    loan: LoanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return loan_service_new.create_loan(db, loan, current_user.id)

@router.get("", response_model=List[LoanResponse])
async def get_user_loans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return loan_service_new.get_user_loans(db, current_user.id)

@router.get("/{loan_id}", response_model=LoanResponse)
async def get_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    loan = loan_service_new.get_loan_by_id(db, loan_id, current_user.id)
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
    result = loan_service_new.process_payment(db, loan_id, payment, current_user.id)
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
    loan = loan_service_new.get_loan_by_id(db, loan_id, current_user.id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return db.query(Payment).filter(Payment.loan_id == loan_id).all()

@router.get("/{loan_id}/status", response_model=LoanStatusResponse)
async def get_loan_status(
    loan_id: UUID = Path(..., description="The unique identifier of the loan"),
    db: Session = Depends(get_db)
):
    """ Get current loan status including balance and next due date
    Returns: LoanStatusResponse with loanId, balance, nextDueDate, and status
    """
    logger.info(f"GET /api/loans/{loan_id}/status - Retrieving loan status")
    try:
        balance, next_due_date, loan_status = LoanService.calculate_remaining_balance(db, loan_id)
        response = LoanStatusResponse(
            loanId=loan_id,
            balance=balance,
            nextDueDate=next_due_date,
            status=loan_status
        )
        logger.info(f"Successfully retrieved status for loan {loan_id}")
        return response
    except ValueError as e:
        if "Loan not found" in str(e):
            logger.warning(f"Loan not found: {loan_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Loan not found"}
            )
        raise
    except Exception as e:
        logger.error(f"Database error retrieving loan status for {loan_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Internal server error"}
        )
