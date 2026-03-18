from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.db.models import Transaction, Account
from backend.schemas.transaction import TransferRequest
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, Any

class TransferService:
    def __init__(self, db: Session):
        self.db = db

    def _get_today_range(self) -> (datetime, datetime):
        """Get today's start and end datetime UTC"""
        now = datetime.utcnow()
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        return start, end

    def _get_month_range(self) -> (datetime, datetime):
        """Get current month's start and end datetime UTC"""
        now = datetime.utcnow()
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Calculate end of month
        next_month = start.replace(month=start.month + 1) if start.month < 12 else start.replace(year=start.year + 1, month=1)
        end = next_month - timedelta(microseconds=1)

        return start, end

    def _calculate_daily_usage(self, account_id: int) -> Decimal:
        """Calculate total amount transferred from this account today"""
        start, end = self._get_today_range()

        result = self.db.query(
            func.coalesce(func.sum(Transaction.amount), 0)
        ).filter(
            Transaction.from_account_id == account_id,
            Transaction.status == "completed",
            Transaction.created_at >= start,
            Transaction.created_at <= end
        ).scalar()

        return Decimal(str(result))

    def _calculate_monthly_usage(self, account_id: int) -> Decimal:
        """Calculate total amount transferred from this account this month"""
        start, end = self._get_month_range()

        result = self.db.query(
            func.coalesce(func.sum(Transaction.amount), 0)
        ).filter(
            Transaction.from_account_id == account_id,
            Transaction.status == "completed",
            Transaction.created_at >= start,
            Transaction.created_at <= end
        ).scalar()

        return Decimal(str(result))

    def check_transfer_limits(self, account_id: int, amount: Decimal) -> Dict[str, Any]:
        """Check if transfer exceeds daily/monthly limits"""
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account:
            return {"error": "Account not found"}

        daily_used = self._calculate_daily_usage(account_id)
        monthly_used = self._calculate_monthly_usage(account_id)

        daily_remaining = account.daily_transfer_limit - daily_used
        monthly_remaining = account.monthly_transfer_limit - monthly_used

        if amount > daily_remaining:
            return {
                "error": "Transfer exceeds daily limit",
                "limit_type": "daily",
                "limit": account.daily_transfer_limit,
                "used": daily_used,
                "remaining": daily_remaining
            }

        if amount > monthly_remaining:
            return {
                "error": "Transfer exceeds monthly limit",
                "limit_type": "monthly",
                "limit": account.monthly_transfer_limit,
                "used": monthly_used,
                "remaining": monthly_remaining
            }

        return {"allowed": True}

    def transfer_funds(self, transfer_request: TransferRequest) -> Dict[str, Any]:
        """Execute funds transfer with all validations"""
        try:
            # Lock accounts for update to prevent race conditions
            from_account = self.db.query(Account).filter(
                Account.id == transfer_request.from_account_id
            ).with_for_update().first()

            to_account = self.db.query(Account).filter(
                Account.id == transfer_request.to_account_id
            ).with_for_update().first()

            if not from_account or not to_account:
                return {"error": "One or both accounts not found"}

            if not from_account.is_active or not to_account.is_active:
                return {"error": "One or both accounts are inactive"}

            if from_account.balance < transfer_request.amount:
                return {"error": "Insufficient funds"}

            # Check transfer limits
            limit_check = self.check_transfer_limits(
                transfer_request.from_account_id,
                transfer_request.amount
            )
            if "error" in limit_check:
                return limit_check

            # Create transaction record
            transaction = Transaction(
                from_account_id=transfer_request.from_account_id,
                to_account_id=transfer_request.to_account_id,
                amount=transfer_request.amount,
                description=transfer_request.description
            )

            self.db.add(transaction)

            # Update account balances
            from_account.balance -= transfer_request.amount
            to_account.balance += transfer_request.amount

            # Mark transaction as completed
            transaction.status = "completed"

            self.db.commit()

            return {
                "success": True,
                "transaction_id": transaction.id,
                "from_balance": float(from_account.balance),
                "to_balance": float(to_account.balance)
            }

        except Exception as e:
            self.db.rollback()
            return {"error": str(e)}

    def get_daily_limit_status(self, account_id: int) -> Dict[str, float]:
        """Get current daily limit status for an account"""
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account:
            return {"error": "Account not found"}

        used = self._calculate_daily_usage(account_id)
        remaining = account.daily_transfer_limit - used

        return {
            "account_id": account_id,
            "daily_limit": float(account.daily_transfer_limit),
            "used_today": float(used),
            "remaining_today": float(remaining),
            "is_limit_exceeded": remaining <= 0
        }

    def get_monthly_limit_status(self, account_id: int) -> Dict[str, float]:
        """Get current monthly limit status for an account"""
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account:
            return {"error": "Account not found"}

        used = self._calculate_monthly_usage(account_id)
        remaining = account.monthly_transfer_limit - used

        return {
            "account_id": account_id,
            "monthly_limit": float(account.monthly_transfer_limit),
            "used_this_month": float(used),
            "remaining_this_month": float(remaining),
            "is_limit_exceeded": remaining <= 0
        }
