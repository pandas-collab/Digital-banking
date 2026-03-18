from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class InsurancePolicy(BaseModel):
    id: str
    type: str
    premium: float
    coverage: float
    duration: int  # in months
    isActive: bool = True

class PolicyPurchase(BaseModel):
    policyId: str
    userEmail: str

class InsuranceService:
    def __init__(self):
        self.policies: List[InsurancePolicy] = [
            InsurancePolicy(
                id="basic-life",
                type="Basic Life Insurance",
                premium=50,
                coverage=10000,
                duration=12
            ),
            InsurancePolicy(
                id="premium-health",
                type="Premium Health Insurance",
                premium=150,
                coverage=50000,
                duration=12
            ),
            InsurancePolicy(
                id="comprehensive-auto",
                type="Comprehensive Auto Insurance",
                premium=75,
                coverage=25000,
                duration=6
            )
        ]

    def get_all_policies(self) -> List[InsurancePolicy]:
        return [policy for policy in self.policies if policy.isActive]

    def purchase_policy(self, user_email: str, policy_id: str) -> bool:
        policy = next((p for p in self.policies if p.id == policy_id), None)
        if not policy:
            return False
        # Here you would save to database
        return True

insurance_service = InsuranceService()
