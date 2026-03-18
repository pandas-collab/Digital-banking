from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import transfers, accounts, loans, users, auth
from app.db.database import engine, Base
from app.core.config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Core Banking API",
    version="1.0.0",
    description="API for tracking loan status and remaining balance"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(loans.router, prefix="/api/loans", tags=["loans"])
app.include_router(transfers.router, prefix="/api/transfers", tags=["transfers"])
app.include_router(accounts.router, prefix="/api/accounts", tags=["accounts"])

@app.get("/")
async def root():
    return {"message": "Core Banking API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
