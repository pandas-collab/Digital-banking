from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from policy_dto import PolicyCreateDTO
from policy_service import PolicyService
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize services
policy_service = PolicyService()

# Create FastAPI app
app = FastAPI(title="Insurance API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/policies")
async def create_policy(policy_dto: PolicyCreateDTO):
    try:
        # Validate premium < coverage
        if policy_dto.premium >= policy_dto.coverage:
            raise HTTPException(400, "Premium must be less than coverage amount")

        policy = policy_service.create_policy(policy_dto)
        return {
            "success": True,
            "data": policy.to_dict(),
            "message": "Policy created successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Policy creation failed: {str(e)}")
        raise HTTPException(500, "Failed to create policy")

@app.get("/api/policies/{policy_id}")
async def get_policy(policy_id: str):
    policy = policy_service.get_policy(policy_id)
    if not policy:
        raise HTTPException(404, "Policy not found")
    return {"success": True, "data": policy.to_dict()}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
