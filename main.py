from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.transfers import router as transfers_router
from api.database import engine, Base
import logging
import asyncio
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PremiumDeductionService:
    async def deduct_premiums(self):
        """Daily premium deduction service"""
        try:
            logger.info("Starting daily premium deduction process...")
            active_policies = await self._get_active_policies()
            logger.info(f"Found {len(active_policies)} active policies")
            for policy in active_policies:
                await self._process_policy_deduction(policy)
            logger.info("Daily premium deduction completed successfully")
            return True
        except Exception as e:
            logger.error(f"Premium deduction failed: {str(e)}")
            return False

    async def _get_active_policies(self):
        return [
            {"policy_id": "POL001", "user_id": "USER001", "premium": 500.00, "balance": 750.00},
            {"policy_id": "POL002", "user_id": "USER002", "premium": 300.00, "balance": 200.00},
            {"policy_id": "POL003", "user_id": "USER003", "premium": 400.00, "balance": 500.00}
        ]

    async def _process_policy_deduction(self, policy):
        user_id = policy["user_id"]
        premium = policy["premium"]
        balance = policy["balance"]
        if balance >= premium:
            new_balance = balance - premium
            logger.info(f"Deducted ${premium} from user {user_id}. New balance: ${new_balance}")
            await self._update_user_balance(user_id, new_balance)
        else:
            logger.warning(f"Insufficient balance for user {user_id}. Marking as defaulter.")
            await self._mark_defaulter(user_id, policy["policy_id"])

    async def _update_user_balance(self, user_id, new_balance):
        logger.info(f"Updated balance for {user_id}: ${new_balance}")

    async def _mark_defaulter(self, user_id, policy_id):
        logger.warning(f"User {user_id} with policy {policy_id} marked as defaulter")

# Scheduled task runner
async def daily_premium_deduction():
    """Run daily premium deduction at 00:00 UTC"""
    service = PremiumDeductionService()
    while True:
        now = datetime.utcnow()
        next_run = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        wait_seconds = (next_run - now).total_seconds()
        await asyncio.sleep(wait_seconds)
        await service.deduct_premiums()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Core Banking Platform API",
    version="1.0.0",
    description="Simplified banking transfers, loans, and insurance platform"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(daily_premium_deduction())
    logger.info("Scheduled premium deduction task started")

# Include routers
app.include_router(transfers_router)

@app.get("/")
async def root():
    return {"message": "Core Banking Platform API is running"}

@app.get("/health")
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
