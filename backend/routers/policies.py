from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from db import get_session
import models.policy as policy_model
import models.account as account_model
import schemas.policy_schemas as schema
from services.premium_scheduler import register_policy_for_premium
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/v1/policies", tags=["policies"])
SessionDep = Annotated[Session, Depends(get_session)]

@router.post("", response_model=schema.PolicyOut)
def create_policy(body: schema.PolicyCreate, session: SessionDep):
    # basic validation
    if not body.coverage_type:
        raise HTTPException(status_code=422, detail="coverage_type is required")
    account = (
        session.query(account_model.Account)
        .filter(account_model.Account.id == 1) # TODO: tie to logged-in user account
        .first()
    )
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    policy = policy_model.Policy(
        account_id=account.id,
        coverage_type=body.coverage_type,
        coverage_amount=body.coverage_amount,
        premium_monthly=body.premium_monthly,
        next_premium_date=datetime.utcnow() + timedelta(days=30),
    )
    session.add(policy)
    session.commit()
    session.refresh(policy)
    register_policy_for_premium(policy.id, session_factory=get_session)
    return policy

@router.get("/{policy_id}", response_model=schema.PolicyOut)
def get_policy(policy_id: int, session: SessionDep):
    policy = session.get(policy_model.Policy, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy
