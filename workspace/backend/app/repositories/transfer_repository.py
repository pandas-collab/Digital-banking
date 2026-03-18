from typing import Optional, List
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
import uuid

from backend.app.models.transfer import TransferResponse

class TransferRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_transfer(
        self,
        from_account_id: uuid.UUID,
        to_account_id: uuid.UUID,
        amount: float
    ) -> TransferResponse:
        from backend.app.database import Transfer

        transfer = Transfer(
            from_account=from_account_id,
            to_account=to_account_id,
            amount=amount,
            status="PENDING"
        )
        self.db.add(transfer)
        await self.db.flush()
        await self.db.refresh(transfer)

        return TransferResponse(
            id=str(transfer.id),
            fromAccount=str(transfer.from_account),
            toAccount=str(transfer.to_account),
            amount=float(transfer.amount),
            status=transfer.status,
            createdAt=transfer.created_at.isoformat()
        )

    async def get_daily_transfer_sum(
        self,
        from_account_id: uuid.UUID
    ) -> float:
        from backend.app.database import Transfer

        stmt = select(func.sum(Transfer.amount)).where(
            and_(
                Transfer.from_account == from_account_id,
                Transfer.created_at >= datetime.utcnow() - timedelta(days=1),
                Transfer.status.in_(["PENDING", "COMPLETED"])
            )
        )
        result = await self.db.execute(stmt)
        return float(result.scalar() or 0)

    async def update_transfer_status(
        self,
        transfer_id: uuid.UUID,
        status: str
    ) -> bool:
        from backend.app.database import Transfer

        stmt = select(Transfer).where(Transfer.id == transfer_id)
        result = await self.db.execute(stmt)
        transfer = result.scalar_one_or_none()

        if transfer:
            transfer.status = status
            return True
        return False

    async def get_account_balance(self, account_id: uuid.UUID) -> Optional[float]:
        from backend.app.database import Account

        stmt = select(Account.balance).where(Account.id == account_id)
        result = await self.db.execute(stmt)
        balance = result.scalar_one_or_none()
        return float(balance) if balance is not None else None

    async def account_exists(self, account_id: uuid.UUID) -> bool:
        from backend.app.database import Account

        stmt = select(Account.id).where(Account.id == account_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def update_account_balance(
        self,
        account_id: uuid.UUID,
        new_balance: float
    ) -> bool:
        from backend.app.database import Account

        stmt = select(Account).where(Account.id == account_id)
        result = await self.db.execute(stmt)
        account = result.scalar_one_or_none()

        if account:
            account.balance = new_balance
            return True
        return False
