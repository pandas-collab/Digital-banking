from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import httpx
import logging
from typing import Optional
from datetime import datetime, date
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TransferRequest(BaseModel):
    from_account: str
    to_account: str
    amount: float
    description: Optional[str] = ""

class TransferService:
    def __init__(self):
        self.transfers = []
        self.daily_limits = {}

    async def transfer_with_retry(self, req: TransferRequest, max_retries: int = 3) -> dict:
        for attempt in range(max_retries):
            try:
                # Simulate network call with timeout
                async with httpx.AsyncClient(timeout=5.0) as client:
                    # Check daily limit
                    today = date.today()
                    key = f"{req.from_account}:{today}"
                    if key not in self.daily_limits:
                        self.daily_limits[key] = 0

                    if self.daily_limits[key] + req.amount > 1000:
                        raise ValueError("Daily limit exceeded")

                    # Simulate transfer
                    await asyncio.sleep(0.1)

                    transfer = {
                        "id": len(self.transfers) + 1,
                        "from": req.from_account,
                        "to": req.to_account,
                        "amount": req.amount,
                        "description": req.description,
                        "timestamp": datetime.utcnow().isoformat(),
                        "status": "completed"
                    }
                    self.transfers.append(transfer)
                    self.daily_limits[key] += req.amount

                    logger.info(f"Transfer successful: {transfer['id']}")
                    return {"success": True, "data": transfer}

            except httpx.TimeoutException:
                logger.warning(f"Timeout attempt {attempt + 1}/{max_retries}")
                if attempt == max_retries - 1:
                    raise HTTPException(status_code=504, detail="Network timeout")
                await asyncio.sleep(2 ** attempt)

            except Exception as e:
                logger.error(f"Transfer failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))

app = FastAPI()
service = TransferService()

@app.post("/api/transfers")
async def create_transfer(request: TransferRequest):
    return await service.transfer_with_retry(request)

@app.get("/api/transfers")
async def get_transfers(account: Optional[str] = None):
    transfers = service.transfers
    if account:
        transfers = [t for t in transfers if t['from'] == account or t['to'] == account]
    return {"success": True, "data": transfers}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
