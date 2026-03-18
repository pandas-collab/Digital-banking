from sqlalchemy.orm import Session
from models.loan import Loan
from models.account import Account
from services.ledger_service import LedgerService
from schemas.loan_schemas import LoanCreateRequest
import math

class LoanService:
    def __init__(self, db: Session):
        self.db = db
        self.ledger_service = LedgerService(db)

    def create_loan(self, request: LoanCreateRequest, account_id: int) -> Loan:
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account:
            raise ValueError("Account not found")

        monthly_rate = request.interest_rate / 100 / 12
        monthly_repayment = (request.amount * monthly_rate * (1 + monthly_rate) ** request.term_months) / ((1 + monthly_rate) ** request.term_months - 1)
        total_repayment = monthly_repayment * request.term_months
        balance_due = total_repayment

        loan = Loan(
            amount=request.amount,
            interest_rate=request.interest_rate,
            term_months=request.term_months,
            balance_due=balance_due,
            monthly_repayment=monthly_repayment,
            borrower_account_id=account_id
        )
        self.db.add(loan)
        self.db.commit()
        self.db.refresh(loan)

        # Initial ledger entry
        self.ledger_service.insert_ledger_entry(
            entity_type='loan',
            entity_id=loan.id,
            cashflow=request.amount,
            direction='in',
            note={'description': 'Loan disbursement'}
        )

        return loan

    def approve_loan(self, loan_id: int) -> Loan:
        loan = self.db.query(Loan).filter(Loan.id == loan_id).first()
        if not loan:
            raise ValueError("Loan not found")
        loan.status = 'APPROVED'
        self.db.commit()
        return loan

    def get_loan_by_id(self, loan_id: int) -> Loan:
        return self.db.query(Loan).filter(Loan.id == loan_id).first()
