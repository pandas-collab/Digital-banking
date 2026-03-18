from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import loans, users, auth
from app.db.database import engine, Base
from app.core.config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Loan Tracker API",
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

@app.get("/")
async def root():
    return {"message": "Loan Tracker API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
