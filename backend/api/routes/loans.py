from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from typing import List

from backend.database.connection import get_db
from backend.middleware.auth import get_current_user
from backend.models.loan import LoanRequest, LoanResponse
from backend.services.loan_service import LoanService
from backend.models.user import User

router = APIRouter(prefix="/api/loans", tags=["loans"])
logger = logging.getLogger(__name__)

@router.post("", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
async def create_loan(
    loan_request: LoanRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new loan application."""
    try:
        loan_service = LoanService()

        # Additional validation
        if not (6 <= loan_request.termMonths <= 60):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Term must be between 6 and 60 months"
            )

        # Create loan
        loan = await loan_service.create_loan(
            db=db,
            user_id=current_user.id,
            amount=loan_request.amount,
            term_months=loan_request.termMonths
        )

        # Simple business rule: auto-approve loans under $5000
        if loan.amount < 5000:
            loan = await loan_service.approve_loan(db, loan.id)

        return LoanResponse(
            id=str(loan.id),
            userId=str(loan.user_id),
            amount=loan.amount,
            termMonths=loan.term_months,
            status=loan.status,
            approvedAt=loan.approved_at.isoformat() if loan.approved_at else None,
            createdAt=loan.created_at.isoformat() if loan.created_at else None
        )

    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Loan creation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error creating loan: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create loan"
        )

@router.get("", response_model=List[LoanResponse])
async def get_loans(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all loans for the current user."""
    try:
        loan_service = LoanService()
        loans = await loan_service.get_loans_by_user(db, current_user.id)

        return [
            LoanResponse(
                id=str(loan.id),
                userId=str(loan.user_id),
                amount=loan.amount,
                termMonths=loan.term_months,
                status=loan.status,
                approvedAt=loan.approved_at.isoformat() if loan.approved_at else None,
                createdAt=loan.created_at.isoformat() if loan.created_at else None
            )
            for loan in loans
        ]
    except Exception as e:
        logger.error(f"Error fetching loans: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch loans"
        )

@router.get("/{loan_id}/status")
async def get_loan_status(
    loan_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get detailed loan status including repayment schedule."""
    from uuid import UUID

    try:
        loan_uuid = UUID(loan_id)
        loan_service = LoanService()
        loan = await loan_service.get_loan_by_id(db, loan_uuid)

        if not loan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Loan not found"
            )

        if str(loan.user_id) != str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )

        # Calculate repayment schedule (simplified - equal monthly payments)
        monthly_payment = loan.amount * (1.05 / loan.term_months)  # 5% interest
        from datetime import timedelta

        schedule = []
        base_date = loan.approved_at or loan.created_at
        for month in range(loan.term_months):
            due_date = base_date + timedelta(days=30 * (month + 1))
            schedule.append({
                "dueDate": due_date.isoformat(),
                "amount": round(monthly_payment, 2)
            })

        return {
            "balance": loan.amount,  # Simplified - total amount
            "nextDueDate": schedule[0]["dueDate"] if schedule else None,
            "status": "ACTIVE" if loan.status == "APPROVED" else loan.status,
            "repaymentSchedule": schedule
        }

    except HTTPException:
        raise
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid loan ID format"
        )
    except Exception as e:
        logger.error(f"Error fetching loan status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch loan status"
        )
