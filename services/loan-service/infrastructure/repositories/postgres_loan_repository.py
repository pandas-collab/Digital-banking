from typing import List, Optional
import psycopg2
from domain.models.loan_application import LoanApplication
from domain.repositories.loan_application_repository import LoanApplicationRepository
from decimal import Decimal

class PostgresLoanApplicationRepository(LoanApplicationRepository):
    def __init__(self):
        self.connection_string = "dbname=loan_service user=postgres password=postgres host=localhost"

    def _get_connection(self):
        return psycopg2.connect(self.connection_string)

    def create(self, application: LoanApplication) -> LoanApplication:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO loan_applications
                    (user_id, amount, term_months, interest_rate, status, purpose,
                     annual_income, employment_status, credit_score)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id, submitted_at
                """, (
                    application.user_id, application.amount, application.term_months,
                    application.interest_rate, application.status, application.purpose,
                    application.annual_income, application.employment_status,
                    application.credit_score
                ))

                result = cur.fetchone()
                application.id = str(result[0])
                application.submitted_at = result[1]

        return application

    def get_by_id(self, application_id: str) -> Optional[LoanApplication]:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM loan_applications WHERE id = %s
                """, (application_id,))

                row = cur.fetchone()
                if not row:
                    return None

                return self._row_to_application(row)

    def get_by_user_id(self, user_id: str) -> List[LoanApplication]:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM loan_applications WHERE user_id = %s
                    ORDER BY submitted_at DESC
                """, (user_id,))

                return [self._row_to_application(row) for row in cur.fetchall()]

    def update(self, application: LoanApplication) -> LoanApplication:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE loan_applications
                    SET status = %s, credit_score = %s, reviewed_at = %s, approved_at = %s
                    WHERE id = %s
                """, (
                    application.status, application.credit_score,
                    application.reviewed_at, application.approved_at,
                    application.id
                ))

        return application

    def get_all(self, limit: int = 100, offset: int = 0) -> List[LoanApplication]:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM loan_applications
                    ORDER BY submitted_at DESC
                    LIMIT %s OFFSET %s
                """, (limit, offset))

                return [self._row_to_application(row) for row in cur.fetchall()]

    def _row_to_application(self, row) -> LoanApplication:
        return LoanApplication(
            id=str(row[0]),
            user_id=str(row[1]),
            amount=Decimal(str(row[2])),
            term_months=row[3],
            interest_rate=Decimal(str(row[4])),
            status=row[5],
            purpose=row[6],
            annual_income=Decimal(str(row[7])),
            employment_status=row[8],
            credit_score=row[9],
            submitted_at=row[10],
            reviewed_at=row[11],
            approved_at=row[12]
        )
