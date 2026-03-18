import logging
from typing import List
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, conint
from db import get_db_session
from ledger_service import LedgerService

logger = logging.getLogger("ledger")
router = APIRouter(prefix="/ledger")

class LedgerEntryResponse(BaseModel):
    ledger_id: int
    event_type: str
    account_id: int
    amount: float
    balance_snapshot: float
    metadata: dict
    created_at: str

    class Config:
        orm_mode = True

@router.get("", response_model=List[LedgerEntryResponse])
def get_ledger(account_id: int = Query(..., gt=0)):
    if account_id <= 0:
        raise HTTPException(status_code=422, detail="invalid account_id")

    session = get_db_session()
    entries = LedgerService(session).fetch_ledger(account_id)
    logger.info("ledger fetch for account_id=%s rows=%d", account_id, len(entries))
    return entries
