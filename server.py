from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta
import logging
import os

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup
DB_URL = os.getenv("DATABASE_URL", "sqlite:///./banking.db")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if "sqlite" in DB_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, unique=True, index=True)
    balance = Column(Float, default=0.0)
    daily_limit = Column(Float, default=1000.0)

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    from_account = Column(String, index=True)
    to_account = Column(String, index=True)
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# Pydantic models
class TransferRequest(BaseModel):
    from_account: str
    to_account: str
    amount: float = Field(gt=0)

class TransferResponse(BaseModel):
    success: bool
    message: str
    transaction_id: int = None

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI app
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/transfer", response_model=TransferResponse)
async def transfer_funds(request: TransferRequest, db: Session = Depends(get_db)):
    try:
        # Validate accounts exist
        from_acc = db.query(Account).filter(Account.account_number == request.from_account).first()
        to_acc = db.query(Account).filter(Account.account_number == request.to_account).first()

        if not from_acc or not to_acc:
            raise HTTPException(status_code=404, detail="Account not found")

        # Check if same account
        if request.from_account == request.to_account:
            raise HTTPException(status_code=400, detail="Cannot transfer to same account")

        # Check daily limit
        today = datetime.utcnow().date()
        daily_transfers = db.query(Transaction).filter(
            Transaction.from_account == request.from_account,
            Transaction.timestamp >= datetime.combine(today, datetime.min.time())
        ).all()
        daily_amount = sum(t.amount for t in daily_transfers)

        if daily_amount + request.amount > from_acc.daily_limit:
            raise HTTPException(status_code=400, detail="Daily limit exceeded")

        # Check balance
        if from_acc.balance < request.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")

        # Perform transfer
        from_acc.balance -= request.amount
        to_acc.balance += request.amount

        # Create transaction
        transaction = Transaction(
            from_account=request.from_account,
            to_account=request.to_account,
            amount=request.amount
        )
        db.add(transaction)
        db.commit()

        logger.info(f"Transfer successful: {request.amount} from {request.from_account} to {request.to_account}")
        return TransferResponse(success=True, message="Transfer completed", transaction_id=transaction.id)

    except HTTPException as e:
        logger.error(f"Transfer failed: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/transactions/{account}")
async def get_transactions(account: str, db: Session = Depends(get_db)):
    try:
        transactions = db.query(Transaction).filter(
            (Transaction.from_account == account) | (Transaction.to_account == account)
        ).order_by(Transaction.timestamp.desc()).limit(50).all()

        return [{
            "id": t.id,
            "from_account": t.from_account,
            "to_account": t.to_account,
            "amount": t.amount,
            "timestamp": t.timestamp.isoformat()
        } for t in transactions]
    except Exception as e:
        logger.error(f"Error fetching transactions: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch transactions")

@app.get("/api/account/{account}")
async def get_account(account: str, db: Session = Depends(get_db)):
    try:
        acc = db.query(Account).filter(Account.account_number == account).first()
        if not acc:
            raise HTTPException(status_code=404, detail="Account not found")
        return {"account_number": acc.account_number, "balance": acc.balance, "daily_limit": acc.daily_limit}
    except HTTPException as e:
        raise
    except Exception as e:
        logger.error(f"Error fetching account: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch account")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
