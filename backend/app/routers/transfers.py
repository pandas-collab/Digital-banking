from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Transfer, Account
from app.schemas.transfer_schema import TransferCreate, TransferOut
from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/transfers", tags=["transfers"])

@router.post("", response_model=TransferOut)
def create_transfer(body: TransferCreate, db: Session = Depends(get_db)):
    from_acc = db.query(Account).get(body.from_account_id)
    to_acc = db.query(Account).get(body.to_account_id)
    if not from_acc or not to_acc:
        raise HTTPException(400, "Account not found")
    if from_acc.balance < body.amount:
        raise HTTPException(400, "Insufficient funds")
    from_acc.balance -= body.amount
    to_acc.balance += body.amount
    t = Transfer(from_account_id=body.from_account_id, to_account_id=body.to_account_id,
                 amount=body.amount, description=body.description or "")
    db.add(t)
    db.commit()
    return {"transfer_id": t.id, "from_balance": from_acc.balance, "to_balance": to_acc.balance}

@router.get("")
def list_transfers(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    transfers = db.query(Transfer).limit(limit).offset(offset).all()
    return [{"id": t.id, "ts": t.created_at, "amount": t.amount, "description": t.description, "account": f"{t.from_account_id}->{t.to_account_id}"} for t in transfers]
