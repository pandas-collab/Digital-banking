from sqlalchemy.orm import Session
from sqlalchemy import func, and_, case
from uuid import UUID
import logging
from typing import Optional, Tuple
from datetime import date
from decimal import Decimal

from app.models.loan import Loan
from app.models.loan_repayment import LoanRepayment

logger = logging.getLogger(__name__)

class LoanService:
    """Service layer for loan operations including status calculation"""

    @staticmethod
    def calculate_remaining_balance(db: Session, loan_id: UUID) -> Tuple[float, Optional[date], str]:
        """
        Calculate remaining loan balance and determine status

        Args:
            db: Database session
            loan_id: UUID of the loan

        Returns:
            Tuple of (remaining_balance, next_due_date, loan_status)

        Raises:
            ValueError: If loan not found
            Exception: For database errors
        """
        start_time = logging.time() if hasattr(logging, 'time') else None

        try:
            # Fetch loan
            loan = db.query(Loan).filter(Loan.id == loan_id).first()
            if not loan:
                raise ValueError("Loan not found")

            logger.info(f"Processing status for loan {loan_id}")

            # Calculate total paid amount (sum of principal for PAID repayments)
            total_paid_result = db.query(
                func.coalesce(func.sum(LoanRepayment.principal), 0)
            ).filter(
                and_(
                    LoanRepayment.loan_id == loan_id,
                    LoanRepayment.status == "PAID"
                )
            ).scalar()

            total_paid = float(total_paid_result) if total_paid_result else 0.0
            remaining_balance = max(0.0, float(loan.amount) - total_paid)

            logger.debug(f"Loan {loan_id}: Principal paid={total_paid}, balance={remaining_balance}")

            # Find next due date
            next_due_repayment = db.query(LoanRepayment).filter(
                and_(
                    LoanRepayment.loan_id == loan_id,
                    LoanRepayment.status == "DUE"
                )
            ).order_by(LoanRepayment.due_date.asc()).first()

            next_due_date = next_due_repayment.due_date if next_due_repayment else None

            # Determine loan status
            if remaining_balance <= 0:
                status = "CLOSED"
            else:
                # Check for any defaulted repayments
                has_default = db.query(
                    db.query(LoanRepayment).filter(
                        and_(
                            LoanRepayment.loan_id == loan_id,
                            LoanRepayment.status == "DEFAULT"
                        )
                    ).exists()
                ).scalar()

                if has_default:
                    status = "DEFAULT"
                else:
                    status = "ACTIVE"

            if start_time:
                execution_time = logging.time() - start_time
                logger.debug(f"Status calculation for loan {loan_id} took {execution_time:.3f}s")

            return remaining_balance, next_due_date, status

        except Exception as e:
            logger.error(f"Error calculating loan status for {loan_id}: {str(e)}", exc_info=True)
            raise
