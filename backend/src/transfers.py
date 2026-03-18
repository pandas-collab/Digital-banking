from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

from .database import get_db
from .transfer_service import TransferService
from .schemas import TransferRequest, TransferResponse, PaginatedTransferResponse
from .auth import get_current_user

router = APIRouter()

@router.post("/transfers", response_model=TransferResponse)
async def create_transfer(
    request: TransferRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        service = TransferService(db)
        transfer = await service.create_transfer(
            current_user.id,
            request.fromAccount,
            request.toAccount,
            request.amount
        )
        return TransferResponse(
            id=str(transfer.id),
            fromAccount=str(transfer.from_account),
            toAccount=str(transfer.to_account),
            amount=float(transfer.amount),
            status=transfer.status,
            createdAt=transfer.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/transfers", response_model=PaginatedTransferResponse)
async def get_transfers(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        service = TransferService(db)
        transfers, total = service.get_user_transfers(current_user.id, page, size)

        transfer_responses = [
            TransferResponse(
                id=str(t.id),
                fromAccount=str(t.from_account),
                toAccount=str(t.to_account),
                amount=float(t.amount),
                status=t.status,
                createdAt=t.created_at
            )
            for t in transfers
        ]

        return PaginatedTransferResponse(
            data=transfer_responses,
            total=total,
            page=page,
            size=size
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
