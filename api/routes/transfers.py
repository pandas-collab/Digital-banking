from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional
import logging
from api.auth import get_current_user_id
from api.database import get_db
from sqlalchemy.orm import Session
from services.transfer_service import TransferService
from schemas.transfer_dto import PaginatedTransfersResponse

router = APIRouter(prefix="/api/transfers", tags=["transfers"])
logger = logging.getLogger(__name__)

@router.get("", response_model=PaginatedTransfersResponse)
async def get_transfers(
    page: int = Query(0, ge=0, description="Zero-based page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get paginated transfer history for authenticated user

    Args:
        page: Zero-based page number (default: 0)
        size: Items per page, max 100 (default: 10)

    Returns:
        PaginatedTransfersResponse with transfer data and total pages
    """
    try:
        service = TransferService(db)
        content, total_pages = service.get_user_transfers(
            user_id=user_id,
            page=page,
            size=size
        )

        return PaginatedTransfersResponse(
            content=content,
            totalPages=total_pages
        )

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching transfers: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
