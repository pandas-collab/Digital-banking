from sqlalchemy.orm import Session
from backend.models.policy import Policy
from datetime import datetime, timedelta
import uuid

class InsuranceService:
    @staticmethod
    def get_available_products():
        """Get available insurance products with pricing"""
        return [
            {
                "product_code": "HEALTH_BASIC",
                "name": "Basic Health Insurance",
                "description": "Covers medical expenses up to $50,000",
                "premium": 150.00,
                "coverage_amount": 50000.00,
                "deductible": 500.00,
                "term_months": 12
            },
            {
                "product_code": "AUTO_COMPREHENSIVE",
                "name": "Comprehensive Auto Insurance",
                "description": "Full coverage for vehicle damage and liability",
                "premium": 89.00,
                "coverage_amount": 25000.00,
                "deductible": 1000.00,
                "term_months": 12
            },
            {
                "product_code": "HOME_PROTECT",
                "name": "Home Protection Plan",
                "description": "Property and liability coverage for homeowners",
                "premium": 42.00,
                "coverage_amount": 100000.00,
                "deductible": 2500.00,
                "term_months": 12
            }
        ]

    @staticmethod
    def create_policy(db: Session, user_id: str, product_code: str):
        """Create a new insurance policy for the user"""
        products = InsuranceService.get_available_products()
        product = next((p for p in products if p['product_code'] == product_code), None)

        if not product:
            raise ValueError("Invalid product code")

        # Generate unique policy number
        policy_number = f"POL-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"

        policy = Policy(
            user_id=user_id,
            policy_number=policy_number,
            product_code=product_code,
            premium=product['premium'],
            coverage_amount=product['coverage_amount'],
            deductible=product['deductible'],
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=365),
            status='ACTIVE'
        )

        db.add(policy)
        db.commit()
        db.refresh(policy)

        return {
            "success": True,
            "policy": {
                "id": policy.id,
                "policy_number": policy.policy_number,
                "product": product,
                "start_date": policy.start_date.isoformat(),
                "end_date": policy.end_date.isoformat(),
                "premium": policy.premium,
                "coverage_amount": policy.coverage_amount
            }
        }
