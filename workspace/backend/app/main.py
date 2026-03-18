from fastapi import FastAPI
from app.db import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Banking System",
    description="Core banking platform API",
    version="1.0.0"
)

# Import and include routers
from app.api.v1.endpoints import ledger
app.include_router(ledger.router)
