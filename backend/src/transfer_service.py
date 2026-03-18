from sqlalchemy.orm import Session
from decimal import Decimal
from uuid import UUID
import uuid

from .models import Transfer, Account, TransferStatus
from .ledger_service import LedgerService
from .database import Base

class TransferService:
    def __init__(self, db: Session):
        self.db = db
        self.ledger = LedgerService(db)

    async def create_transfer(self, user_id: uuid.UUID, from_account_str: str,
                             to_account_str: str, amount: Decimal) -> Transfer:
        from_account_uuid = uuid.UUID(from_account_str)
        to_account_uuid = uuid.UUID(to_account_str)

        # Validate accounts exist and belong to the user
        from_account = self.db.query(Account).filter(
            Account.id == from_account_uuid,
            Account.user_id == user_id
        ).first()

        if not from_account:
            raise ValueError("From account not found or does not belong to user")

        to_account = self.db.query(Account).filter(
            Account.id == to_account_uuid,
            Account.user_id == user_id
        ).first()

        if not to_account:
            raise ValueError("To account not found or does not belong to user")

        if from_account_uuid == to_account_uuid:
            raise ValueError("Cannot transfer to the same account")

        # Check sufficient funds
        if from_account.balance < amount:
            raise ValueError("Insufficient funds")

        # Create transfer record
        transfer = Transfer(
            from_account=from_account_uuid,
            to_account=to_account_uuid,
            amount=amount,
            status=TransferStatus.PENDING
        )

        self.db.add(transfer)
        self.db.commit()

        try:
            # Update balances
            from_account.balance -= amount
            to_account.balance += amount

            self.ledger.record_transfer(transfer.id, from_account_uuid, to_account_uuid, amount)

            transfer.status = TransferStatus.COMPLETED
            self.db.commit()

            return transfer
        except Exception as e:
            transfer.status = TransferStatus.FAILED
            self.db.commit()
            raise e

    def get_user_transfers(self, user_id: uuid.UUID, page: int, size: int):
        query = self.db.query(Transfer)\
            .join(Account, (Transfer.from_account == Account.id) | (Transfer.to_account == Account.id))\
            .filter(Account.user_id == user_id)\
            .distinct()\
            .order_by(Transfer.created_at.desc())

        total = query.count()
        transfers = query.offset((page - 1) * size).limit(size).all()

        return transfers, total
