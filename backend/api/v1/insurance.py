from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from backend.services.database import get_db
from backend.services.insurance_service import InsuranceService
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/insurance", tags=["Insurance"])

class PurchaseRequest(BaseModel):
    product_code: str
    user_id: str

@router.get("/products")
async def get_products():
    """Get all available insurance products"""
    try:
        products = InsuranceService.get_available_products()
        return {"products": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/purchase")
async def purchase_insurance(
    request: PurchaseRequest,
    db: Session = Depends(get_db),
    x_user_id: str = Header(default="test-user-123")
):
    """Purchase an insurance policy"""
    try:
        # Use authenticated user_id if available, otherwise fall back to header
        user_id = request.user_id or x_user_id

        if not request.product_code:
            raise HTTPException(status_code=400, detail="Product code is required")

        result = InsuranceService.create_policy(db, user_id, request.product_code)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/policies/{user_id}")
async def get_user_policies(user_id: str, db: Session = Depends(get_db)):
    """Get all policies for a user"""
    try:
        from backend.models.policy import Policy
        policies = db.query(Policy).filter(
            Policy.user_id == user_id,
            Policy.status == 'ACTIVE'
        ).all()

        if not policies:
            return {"policies": [], "message": "No active policies found"}

        active_products = InsuranceService.get_available_products()
        user_policies = []

        for policy in policies:
            product = next(
                (p for p in active_products if p['product_code'] == policy.product_code),
                None
            )
            if product:
                user_policies.append({
                    "id": policy.id,
                    "policy_number": policy.policy_number,
                    "product": product,
                    "start_date": policy.start_date.isoformat(),
                    "end_date": policy.end_date.isoformat(),
                    "premium": policy.premium,
                    "coverage_amount": policy.coverage_amount,
                    "status": policy.status
                })

        return {"policies": user_policies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
