import logging
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from decimal import Decimal
import asyncio
from . import loan, account, ledger_service

logger = logging.getLogger(__name__)

async def apply_for_loan(db: Session, user_id: int, amount: float, term_months: int) -> loan.Loan:
    """Apply for a new loan with validation"""
    try:
        if amount <= 0 or term_months <= 0:
            raise ValueError("Invalid loan parameters")

        new_loan = loan.Loan(
            user_id=user_id,
            principal=float(amount),
            remaining_principal=float(amount),
            interest_rate=0.12,  # 12% annual
            term_months=term_months,
            status="PENDING",
            created_at=datetime.utcnow(),
            next_payment_date=datetime.utcnow() + timedelta(days=30)
        )

        db.add(new_loan)
        db.commit()
        db.refresh(new_loan)

        logger.info(f"Loan {new_loan.id} applied for user {user_id} amount {amount}")
        return new_loan

    except Exception as e:
        db.rollback()
        logger.error(f"Loan application failed: {e}")
        raise

async def process_repayment(db: Session, loan_id: int, amount: float) -> dict:
    """Process loan repayment with validation"""
    try:
        loan_obj = db.query(loan.Loan).filter(loan.Loan.id == loan_id).first()
        if not loan_obj:
            raise ValueError("Loan not found")

        if loan_obj.status not in ["APPROVED", "ACTIVE"]:
            raise ValueError("Loan not active")

        if amount <= 0:
            raise ValueError("Invalid repayment amount")

        # Calculate payment
        interest_payment = loan_obj.remaining_principal * (loan_obj.interest_rate / 12)
        principal_payment = min(amount - interest_payment, loan_obj.remaining_principal)

        # Update loan
        loan_obj.remaining_principal -= principal_payment
        loan_obj.total_repaid += amount

        if loan_obj.remaining_principal <= 0.01:
            loan_obj.status = "COMPLETED"
            loan_obj.completed_at = datetime.utcnow()

        # Create ledger entry
        await ledger_service.create_ledger_entry(
            db,
            loan_obj.user_id,
            f"LOAN_REPAYMENT_{loan_id}",
            -amount,
            f"Loan repayment for loan {loan_id}"
        )

        db.commit()

        logger.info(f"Repayment processed: loan {loan_id} amount {amount}")
        return {
            "success": True,
            "remaining_balance": loan_obj.remaining_principal,
            "status": loan_obj.status
        }

    except Exception as e:
        db.rollback()
        logger.error(f"Repayment processing failed: {e}")
        raise

async def handle_defaulters(db: Session) -> int:
    """Identify and process defaulters"""
    try:
        overdue_loans = db.query(loan.Loan).filter(
            loan.Loan.status == "ACTIVE",
            loan.Loan.next_payment_date < datetime.utcnow() - timedelta(days=30)
        ).all()

        for loan_obj in overdue_loans:
            loan_obj.status = "DEFAULT"
            loan_obj.defaulted_at = datetime.utcnow()
            logger.warning(f"Loan {loan_obj.id} marked as default")

        db.commit()
        return len(overdue_loans)

    except Exception as e:
        db.rollback()
        logger.error(f"Default handling failed: {e}")
        raise
