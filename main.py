from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime, timedelta
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./loans.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI app
app = FastAPI(title="Loan Management System")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Loan model
class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    applicant_name = Column(String, index=True)
    email = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    term_months = Column(Integer, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    next_payment_date = Column(DateTime)
    balance = Column(Float, nullable=False)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class LoanApplication(BaseModel):
    applicant_name: str
    email: EmailStr
    amount: float
    interest_rate: float = 5.5
    term_months: int

    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v

    @validator('term_months')
    def validate_term(cls, v):
        if v < 1 or v > 360:
            raise ValueError('Term must be between 1 and 360 months')
        return v

class LoanResponse(BaseModel):
    id: int
    applicant_name: str
    email: str
    amount: float
    interest_rate: float
    term_months: int
    status: str
    balance: float
    created_at: datetime

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API endpoints
@app.post("/api/loans", response_model=LoanResponse)
async def create_loan(loan: LoanApplication, db: Session = Depends(get_db)):
    try:
        logger.info(f"Creating loan for {loan.applicant_name}: ${loan.amount}")

        # Simple approval logic based on amount
        status = "approved" if loan.amount <= 10000 else "pending"

        db_loan = Loan(
            applicant_name=loan.applicant_name,
            email=loan.email,
            amount=loan.amount,
            interest_rate=loan.interest_rate,
            term_months=loan.term_months,
            status=status,
            balance=loan.amount
        )

        if status == "approved":
            # Set next payment 30 days from now
            db_loan.next_payment_date = datetime.utcnow() + timedelta(days=30)

        db.add(db_loan)
        db.commit()
        db.refresh(db_loan)

        return LoanResponse(
            id=db_loan.id,
            applicant_name=db_loan.applicant_name,
            email=db_loan.email,
            amount=db_loan.amount,
            interest_rate=db_loan.interest_rate,
            term_months=db_loan.term_months,
            status=db_loan.status,
            balance=db_loan.balance,
            created_at=db_loan.created_at
        )

    except Exception as e:
        logger.error(f"Error creating loan: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/loans", response_model=list[LoanResponse])
async def list_loans(db: Session = Depends(get_db)):
    try:
        loans = db.query(Loan).all()
        return [LoanResponse(
            id=l.id,
            applicant_name=l.applicant_name,
            email=l.email,
            amount=l.amount,
            interest_rate=l.interest_rate,
            term_months=l.term_months,
            status=l.status,
            balance=l.balance,
            created_at=l.created_at
        ) for l in loans]
    except Exception as e:
        logger.error(f"Error listing loans: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/loans/{loan_id}/repayment")
async def process_repayment(loan_id: int, amount: float, db: Session = Depends(get_db)):
    try:
        loan = db.query(Loan).filter(Loan.id == loan_id).first()
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")

        if loan.status != "approved":
            raise HTTPException(status_code=400, detail="Loan not approved for repayment")

        if amount <= 0:
            raise HTTPException(status_code=400, detail="Invalid payment amount")

        loan.balance = max(0, loan.balance - amount)

        if loan.balance == 0:
            loan.status = "completed"

        db.commit()
        return {"success": True, "new_balance": loan.balance, "status": loan.status}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing repayment: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def health_check():
    return {"status": "healthy", "message": "Loan Management System is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
