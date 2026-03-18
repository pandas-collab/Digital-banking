from sqlalchemy.orm import Session
from models.policy import Policy
from schemas.policy import PolicyCreate
from datetime import date, timedelta

class PolicyService:
    @staticmethod
    def create_policy(db: Session, policy_create: PolicyCreate, account_id: int):
        next_premium = date.today() + timedelta(days=30)
        db_policy = Policy(
            account_id=account_id,
            coverage_type=policy_create.coverage_type,
            coverage_amount=policy_create.coverage_amount,
            premium_monthly=policy_create.premium_monthly,
            status="active",
            next_premium_date=next_premium,
            balance_due=0.00
        )
        db.add(db_policy)
        db.commit()
        db.refresh(db_policy)
        return db_policy

    @staticmethod
    def get_policy(db: Session, policy_id: int):
        return db.query(Policy).filter(Policy.id == policy_id).first()

    @staticmethod
    def get_policies_by_account(db: Session, account_id: int):
        return db.query(Policy).filter(Policy.account_id == account_id).all()
