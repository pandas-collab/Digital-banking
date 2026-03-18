from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from schemas.policy import PolicyCreate, PolicyResponse, PolicyDetail
from services.policy_service import PolicyService

router = APIRouter(prefix="/api/v1", tags=["policies"])

@router.post("/policies", response_model=PolicyResponse)
def create_policy(policy: PolicyCreate, db: Session = Depends(get_db)):
    # Hardcoded account_id=1 for demo purposes
    db_policy = PolicyService.create_policy(db, policy, account_id=1)
    return PolicyResponse(
        policy_id=db_policy.id,
        status=db_policy.status,
        premium_monthly=float(db_policy.premium_monthly)
    )

@router.get("/policies/{policy_id}", response_model=PolicyDetail)
def get_policy(policy_id: int, db: Session = Depends(get_db)):
    db_policy = PolicyService.get_policy(db, policy_id)
    if not db_policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return PolicyDetail.from_orm(db_policy)
