from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.transfers import router as transfers_router
from api.database import engine, Base
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

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
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(transfers_router)

@app.get("/")
async def root():
    return {"message": "Core Banking Platform API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
