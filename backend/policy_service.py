import logging
from typing import Dict, List, Optional
from policy import Policy
from policy_dto import PolicyCreateDTO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PolicyService:
    def __init__(self):
        self.policies: Dict[str, Policy] = {}

    def create_policy(self, policy_dto: PolicyCreateDTO) -> Policy:
        try:
            policy = Policy(
                plan=policy_dto.plan,
                premium=policy_dto.premium,
                coverage=policy_dto.coverage,
                email=policy_dto.email
            )
            self.policies[policy.id] = policy
            logger.info(f"Policy created: {policy.id} for {policy.email}")
            return policy
        except Exception as e:
            logger.error(f"Policy creation failed: {str(e)}")
            raise e

    def get_policy(self, policy_id: str) -> Optional[Policy]:
        return self.policies.get(policy_id)

    def list_policies(self) -> List[Policy]:
        return list(self.policies.values())
