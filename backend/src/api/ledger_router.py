"""REST endpoints for ledger queries."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.user import User
from src.schemas.ledger import LedgerEntry, LedgerPage
from src.services.ledger_service import LedgerService
from src.auth import get_current_user

router = APIRouter(prefix="/ledger", tags=["ledger"])

@router.get("/", response_model=LedgerPage)
async def list_ledger_entries(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List ledger entries for the authenticated user."""
    account_id = current_user.account_id
    if not account_id:
        raise HTTPException(
            status_code=404,
            detail="User account not found"
        )

    return await LedgerService.get_user_ledger(
        db,
        account_id,
        page=page,
        per_page=per_page
    )

@router.get("/{transfer_id}", response_model=List[LedgerEntry])
async def get_transfer_ledger_entries(
    transfer_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get ledger entries for a specific transfer."""
    entries = await LedgerService.get_transfer_ledger(db, transfer_id)

    # Verify user has access to this transfer
    user_account_id = current_user.account_id
    if not any(
        entry.from_account_id == user_account_id or
        entry.to_account_id == user_account_id
        for entry in entries
    ):
        raise HTTPException(
            status_code=403,
            detail="Access denied to this transfer"
        )

    return entries
