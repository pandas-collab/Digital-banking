from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from backend.api.deps import get_db
from backend.schemas.transaction import (
    TransferRequest,
    TransactionResponse,
    TransactionHistory,
    DailyLimitStatus,
    MonthlyLimitStatus
)
from backend.services.transfer_service import TransferService
from backend.models.transaction import Transaction
from backend.db.session import get_db

router = APIRouter()

@router.post("/transfer", response_model=dict)
def transfer_funds(transfer: TransferRequest, db: Session = Depends(get_db)):
    """Transfer funds between accounts with daily/monthly limit checks"""
    service = TransferService(db)
    result = service.transfer_funds(transfer)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result

@router.get("/transfer/limits/daily/{account_id}", response_model=DailyLimitStatus)
def get_daily_limit_status(account_id: int, db: Session = Depends(get_db)):
    """Get current daily transfer limit status for an account"""
    service = TransferService(db)
    result = service.get_daily_limit_status(account_id)

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return DailyLimitStatus(**result)

@router.get("/transfer/limits/monthly/{account_id}", response_model=MonthlyLimitStatus)
def get_monthly_limit_status(account_id: int, db: Session = Depends(get_db)):
    """Get current monthly transfer limit status for an account"""
    service = TransferService(db)
    result = service.get_monthly_limit_status(account_id)

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return MonthlyLimitStatus(**result)

@router.get("/transactions/history/{account_id}", response_model=TransactionHistory)
def get_transaction_history(
    account_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    transaction_type: str = Query(None),
    db: Session = Depends(get_db)
):
    """Get transaction history for an account"""
    query = db.query(Transaction).filter(
        (Transaction.from_account_id == account_id) |
        (Transaction.to_account_id == account_id)
    )

    if transaction_type:
        query = query.filter(Transaction.transaction_type == transaction_type)

    total_count = query.count()
    offset = (page - 1) * limit

    transactions = query.order_by(
        Transaction.created_at.desc()
    ).offset(offset).limit(limit).all()

    transaction_responses = [
        TransactionResponse(
            id=t.id,
            from_account_id=t.from_account_id,
            to_account_id=t.to_account_id,
            amount=float(t.amount),
            status=t.status,
            transaction_type=t.transaction_type,
            description=t.description,
            created_at=t.created_at.isoformat()
        ) for t in transactions
    ]

    total_pages = (total_count + limit - 1) // limit

    return TransactionHistory(
        transactions=transaction_responses,
        total_count=total_count,
        current_page=page,
        total_pages=total_pages
    )
