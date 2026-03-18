from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from datetime import datetime
import logging

from app.db import get_db
from app.repositories.ledger_repository import LedgerRepository
from app.schemas.ledger import LedgerQueryResponse, LedgerQueryParams

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/api/ledger", response_model=LedgerQueryResponse)
async def get_ledger(
    fromDate: Optional[str] = Query(None, description="Start date (ISO-8601)"),
    toDate: Optional[str] = Query(None, description="End date (ISO-8601)"),
    account: Optional[str] = Query(None, description="Account UUID"),
    type: Optional[str] = Query(None, description="Event type (TRANSFER|LOAN|PREMIUM|REPAYMENT)"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    db: Session = Depends(get_db)
):
    try:
        # Validate parameters
        params = LedgerQueryParams(
            fromDate=fromDate,
            toDate=toDate,
            account=account,
            type=type,
            page=page,
            size=size
        )

        repository = LedgerRepository(db)
        results, total = repository.query_ledger(
            from_date=params.fromDate,
            to_date=params.toDate,
            account_id=params.account,
            event_type=params.type,
            page=params.page,
            size=params.size
        )

        # Convert to response format
        events = []
        for ledger_entry in results:
            event = {
                "id": ledger_entry.id,
                "ts": ledger_entry.ts.isoformat(),
                "account": ledger_entry.account_id,
                "type": ledger_entry.type,
                "amount": float(ledger_entry.amount),
                "meta": ledger_entry.metadata
            }
            events.append(event)

        return {"events": events, "total": total}

    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Internal server error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
