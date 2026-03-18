from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError
import logging
from uuid import UUID

from ...schemas.policy_dto import PolicyCreateRequest, PolicyCreateResponse
from ...services.policy_service import PolicyService
from ...dependencies import get_db, get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["policies"])

@router.post(
    "/policies",
    response_model=PolicyCreateResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Policy created successfully"},
        400: {"description": "Bad request - validation failed"},
        422: {"description": "Unprocessable entity - invalid data format"},
        500: {"description": "Internal server error"}
    }
)
async def create_policy(
    request: Request,
    policy: PolicyCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user)
):
    """Create a new insurance policy for the authenticated user."""
    try:
        logger.info(
            f"Creating policy request: user={current_user_id}, plan={policy.planName}, "
            f"premium={policy.premiumAmount}, coverage={policy.coverageAmount}"
        )

        policy_id = await PolicyService.create_policy(
            user_id=current_user_id,
            policy_data=policy,
            db=db
        )

        return PolicyCreateResponse(policyId=str(policy_id))

    except ValidationError as e:
        logger.warning(f"Validation error: {e.json()}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors()
        )
    except HTTPException as http_exc:
        logger.warning(f"HTTP exception: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(
            f"Unexpected error creating policy for user {current_user_id}: {str(e)}",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@router.get("/policies", response_model=list[dict])
async def get_user_policies(
    db: AsyncSession = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user)
):
    """Get all policies for the authenticated user."""
    policies = await PolicyService.get_user_policies(current_user_id, db)
    return [policy.dict() for policy in policies]
