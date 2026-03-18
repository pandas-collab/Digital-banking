from sqlalchemy.orm import Session
from models.loan import Loan
from models.account import Account
from services.ledger_service import LedgerService
from services.loan_service import LoanService
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class SchedulerService:
    def __init__(self, db: Session):
        self.db = db
        self.ledger_service = LedgerService(db)
        self.loan_service = LoanService(db)

    def process_monthly_repayments(self):
        loans = self.db.query(Loan).filter(Loan.status == 'APPROVED', Loan.balance_due > 0).all()
        for loan in loans:
            account = self.db.query(Account).filter(Account.id == loan.borrower_account_id).first()
            if account.balance >= loan.monthly_repayment:
                # Process repayment
                self.ledger_service.insert_ledger_entry(
                    entity_type='loan',
                    entity_id=loan.id,
                    cashflow=float(loan.monthly_repayment),
                    direction='out',
                    note={'description': 'Monthly repayment'}
                )
                loan.balance_due -= loan.monthly_repayment
            else:
                # Handle missed payment
                logger.warning(f"Loan {loan.id} missed payment. Borrower account {account.id} insufficient balance.")
                loan.status = 'DENIED'  # Mark as DEFAULTER per stub logic
            self.db.commit()
