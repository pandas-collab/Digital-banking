"""Business logic for ledger operations."""

from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.ledger import Ledger
from src.schemas.ledger import LedgerCreate, LedgerEntry, LedgerPage

class LedgerService:
    """Service for handling ledger operations."""

    @staticmethod
    async def create_entry(session: AsyncSession, entry_data: LedgerCreate) -> LedgerEntry:
        """Create an immutable ledger entry."""
        ledger = Ledger(**entry_data.dict())
        session.add(ledger)
        await session.commit()
        await session.refresh(ledger)
        return LedgerEntry.from_orm(ledger)

    @staticmethod
    async def get_user_ledger(
        session: AsyncSession,
        user_account_id: int,
        page: int = 1,
        per_page: int = 20
    ) -> LedgerPage:
        """Get ledger entries for a user (either as sender or recipient)."""
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 20

        offset = (page - 1) * per_page

        # Count total entries
        count_query = select(func.count(Ledger.id)).where(
            (Ledger.from_account_id == user_account_id) |
            (Ledger.to_account_id == user_account_id)
        )
        total_result = await session.execute(count_query)
        total = total_result.scalar()

        # Get paginated entries
        query = (
            select(Ledger)
            .where(
                (Ledger.from_account_id == user_account_id) |
                (Ledger.to_account_id == user_account_id)
            )
            .order_by(Ledger.created_at.desc())
            .offset(offset)
            .limit(per_page)
        )
        result = await session.execute(query)
        items = [LedgerEntry.from_orm(row) for row in result.scalars().all()]

        return LedgerPage(
            items=items,
            total=total,
            page=page,
            per_page=per_page
        )

    @staticmethod
    async def get_transfer_ledger(
        session: AsyncSession,
        transfer_id: int
    ) -> List[LedgerEntry]:
        """Get all ledger entries for a specific transfer."""
        query = (
            select(Ledger)
            .where(Ledger.transfer_id == transfer_id)
            .order_by(Ledger.created_at.asc())
        )
        result = await session.execute(query)
        return [LedgerEntry.from_orm(row) for row in result.scalars().all()]
