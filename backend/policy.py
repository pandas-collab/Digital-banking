from datetime import datetime
import uuid

class Policy:
    def __init__(self, plan: str, premium: float, coverage: float, email: str):
        self.id = str(uuid.uuid4())
        self.plan = plan
        self.premium = premium
        self.coverage = coverage
        self.email = email
        self.created_at = datetime.utcnow().isoformat()
        self.status = "active"
    def to_dict(self):
        return {
            "id": self.id,
            "plan": self.plan,
            "premium": self.premium,
            "coverage": self.coverage,
            "email": self.email,
            "created_at": self.created_at,
            "status": self.status
        }
