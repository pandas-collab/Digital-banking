import pytest
from decimal import Decimal
from datetime import datetime, timedelta
from backend.services.transfer_service import TransferService
from backend.models.transaction import Transaction
from backend.models.account import Account

class TestTransferService:

    @pytest.fixture
    def service(self, db_session):
        return TransferService(db_session)

    def test_transfer_within_limits(self, service, db_session):
        # Create test accounts
        from_account = Account(user_id=1, account_number="FROM001", daily_transfer_limit=Decimal('1000'), monthly_transfer_limit=Decimal('10000'))
        to_account = Account(user_id=2, account_number="TO001")

        from_account.balance = Decimal('500')
        to_account.balance = Decimal('0')

        db_session.add_all([from_account, to_account])
        db_session.commit()

        transfer = TransferRequest(
            from_account_id=from_account.id,
            to_account_id=to_account.id,
            amount=Decimal('100')
        )

        result = service.transfer_funds(transfer)

        assert result["success"] is True
        assert float(from_account.balance) == 400.0
        assert float(to_account.balance) == 100.0

    def test_transfer_exceeds_daily_limit(self, service, db_session):
        from_account = Account(user_id=1, account_number="FROM002", daily_transfer_limit=Decimal('500'), monthly_transfer_limit=Decimal('10000'))
        to_account = Account(user_id=2, account_number="TO002")

        from_account.balance = Decimal('1000')
        to_account.balance = Decimal('0')

        db_session.add_all([from_account, to_account])
        db_session.commit()

        # Create existing transaction to hit daily limit
        existing_tx = Transaction(
            from_account_id=from_account.id,
            to_account_id=to_account.id,
            amount=Decimal('400'),
            status="completed"
        )
        db_session.add(existing_tx)
        db_session.commit()

        transfer = TransferRequest(
            from_account_id=from_account.id,
            to_account_id=to_account.id,
            amount=Decimal('200')  # Would exceed daily limit
        )

        result = service.transfer_funds(transfer)

        assert "error" in result
        assert "daily limit" in result["error"].lower()

    def test_insufficient_funds(self, service, db_session):
        from_account = Account(user_id=1, account_number="FROM003", daily_transfer_limit=Decimal('1000'))
        to_account = Account(user_id=2, account_number="TO003")

        from_account.balance = Decimal('50')

        db_session.add_all([from_account, to_account])
        db_session.commit()

        transfer = TransferRequest(
            from_account_id=from_account.id,
            to_account_id=to_account.id,
            amount=Decimal('100')
        )

        result = service.transfer_funds(transfer)

        assert "error" in result
        assert "insufficient" in result["error"].lower()
