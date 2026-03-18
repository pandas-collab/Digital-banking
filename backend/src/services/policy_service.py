import logging
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from decimal import Decimal
from ..models.policy import Policy
from ..schemas.policy_dto import PolicyCreateRequest, PolicyDetail

logger = logging.getLogger(__name__)

class PolicyService:
    @staticmethod
    async def create_policy(
        user_id: UUID,
        policy_data: PolicyCreateRequest,
        db: AsyncSession
    ) -> UUID:
        """Create a new insurance policy for the user."""
        try:
            # Validate premium vs coverage
            if policy_data.premiumAmount > policy_data.coverageAmount * 0.05:
                logger.warning(
                    f"Premium amount {policy_data.premiumAmount} exceeds 5% limit for coverage {policy_data.coverageAmount}"
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Premium amount exceeds 5% limit of coverage amount"
                )

            policy = Policy(
                user_id=user_id,
                plan_name=policy_data.planName,
                premium_amount=Decimal(str(policy_data.premiumAmount)),
                coverage_amount=Decimal(str(policy_data.coverageAmount))
            )

            db.add(policy)
            await db.commit()
            await db.refresh(policy)

            logger.info(f"Policy created: policyId={policy.id}, userId={user_id}")
            return policy.id

        except IntegrityError as e:
            await db.rollback()
            if "unique" in str(e.orig).lower():
                logger.warning(
                    f"Duplicate policy name '{policy_data.planName}' for user {user_id}"
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Policy with plan name '{policy_data.planName}' already exists for this user"
                )
            else:
                logger.error(f"Database integrity error: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid policy data"
                )
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            logger.error(
                f"Failed to create policy for user {user_id}: {str(e)}",
                exc_info=True
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error while creating policy"
            )

    @staticmethod
    async def get_user_policies(
        user_id: UUID,
        db: AsyncSession
    ) -> list[PolicyDetail]:
        """Get all policies for a user."""
        result = await db.execute(
            select(Policy).where(Policy.user_id == user_id)
        )
        policies = result.scalars().all()
        return [
            PolicyDetail(
                id=policy.id,
                userId=policy.user_id,
                planName=policy.plan_name,
                premiumAmount=policy.premium_amount,
                coverageAmount=policy.coverage_amount,
                status=policy.status,
                createdAt=policy.created_at.isoformat()
            )
            for policy in policies
        ]
