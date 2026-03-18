from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.transfer import TransferRequest, TransferResponse
from backend.app.services.transfer_service import TransferService
from backend.app.database import get_db_async

router = APIRouter(prefix="/api", tags=["transfers"])

@router.post(
    "/transfers",
    response_model=TransferResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_transfer(
    transfer_request: TransferRequest,
    db: AsyncSession = Depends(get_db_async)
) -> TransferResponse:
    """
    Create a new fund transfer between accounts.

    - Validates input parameters
    - Checks account existence and balance
    - Enforces 500K daily limit
    - Performs atomic transfer operation
    """
    service = TransferService(db)

    try:
        result = await service.create_transfer(transfer_request)
        return result

    except ValueError as e:
        if str(e) in ["Source account not found", "Destination account not found"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        elif str(e) in ["Insufficient funds", "Daily transfer limit exceeded"]:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e)
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during transfer"
        )
