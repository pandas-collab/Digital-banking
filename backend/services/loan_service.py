import logging
from typing import Optional
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from backend.models.loan import LoanInDB

logger = logging.getLogger(__name__)

class LoanService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def create_loan(
        self,
        db: AsyncSession,
        user_id: UUID,
        amount: float,
        term_months: int
    ) -> LoanInDB:
        """Create a new loan application."""
        self.logger.info(f"Creating loan for user {user_id}: amount={amount}, term={term_months}")

        async with db.begin():
            result = await db.execute(
                text("""
                    INSERT INTO loans (user_id, amount, term_months, status)
                    VALUES (:user_id, :amount, :term_months, 'PENDING')
                    RETURNING id, user_id, amount, term_months, status, approved_at, created_at
                """),
                {
                    "user_id": str(user_id),
                    "amount": amount,
                    "term_months": term_months
                }
            )
            row = result.fetchone()
            if not row:
                raise ValueError("Failed to create loan")

            loan = LoanInDB(
                id=row[0],
                user_id=row[1],
                amount=float(row[2]),
                term_months=row[3],
                status=row[4],
                approved_at=row[5],
                created_at=row[6]
            )

            self.logger.info(f"Created loan {loan.id} for user {user_id}")
            return loan

    async def approve_loan(self, db: AsyncSession, loan_id: UUID) -> LoanInDB:
        """Approve a loan application."""
        self.logger.info(f"Approving loan {loan_id}")

        async with db.begin():
            result = await db.execute(
                text("""
                    UPDATE loans
                    SET status = 'APPROVED', approved_at = :now
                    WHERE id = :loan_id
                    RETURNING id, user_id, amount, term_months, status, approved_at, created_at
                """),
                {"loan_id": str(loan_id), "now": datetime.now(timezone.utc)}
            )
            row = result.fetchone()
            if not row:
                raise ValueError(f"Loan {loan_id} not found")

            loan = LoanInDB(
                id=row[0],
                user_id=row[1],
                amount=float(row[2]),
                term_months=row[3],
                status=row[4],
                approved_at=row[5],
                created_at=row[6]
            )

            self.logger.info(f"Approved loan {loan_id}")
            return loan

    async def get_loans_by_user(self, db: AsyncSession, user_id: UUID) -> list[LoanInDB]:
        """Get all loans for a user."""
        self.logger.info(f"Fetching loans for user {user_id}")

        result = await db.execute(
            text("""
                SELECT id, user_id, amount, term_months, status, approved_at, created_at
                FROM loans
                WHERE user_id = :user_id
                ORDER BY created_at DESC
            """),
            {"user_id": str(user_id)}
        )

        loans = []
        for row in result.fetchall():
            loans.append(LoanInDB(
                id=row[0],
                user_id=row[1],
                amount=float(row[2]),
                term_months=row[3],
                status=row[4],
                approved_at=row[5],
                created_at=row[6]
            ))

        return loans

    async def get_loan_by_id(self, db: AsyncSession, loan_id: UUID) -> Optional[LoanInDB]:
        """Get a loan by ID."""
        self.logger.info(f"Fetching loan {loan_id}")

        result = await db.execute(
            text("""
                SELECT id, user_id, amount, term_months, status, approved_at, created_at
                FROM loans
                WHERE id = :loan_id
            """),
            {"loan_id": str(loan_id)}
        )

        row = result.fetchone()
        if not row:
            return None

        return LoanInDB(
            id=row[0],
            user_id=row[1],
            amount=float(row[2]),
            term_months=row[3],
            status=row[4],
            approved_at=row[5],
            created_at=row[6]
        )
