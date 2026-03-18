from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session
from uuid import UUID
import logging
from typing import Optional

from app.schemas.loan_status import LoanStatusResponse
from app.services.loan_service import LoanService
from app.dependencies import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/loans", tags=["loans"])

@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_loan(create_request: dict, db: Session = Depends(get_db)):
    """Create a new loan - placeholder for POST /api/loans"""
    # Implementation would go here
    return {"loanId": "placeholder", "status": "PENDING"}

@router.get("/{loan_id}/status", response_model=LoanStatusResponse)
async def get_loan_status(
    loan_id: UUID = Path(..., description="The unique identifier of the loan"),
    db: Session = Depends(get_db)
):
    """
    Get current loan status including balance and next due date

    Returns:
        LoanStatusResponse with loanId, balance, nextDueDate, and status
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
