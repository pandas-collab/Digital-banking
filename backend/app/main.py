from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import transfers, accounts, loans, users, auth

app = FastAPI(title="Core Banking API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transfers.router)
app.include_router(accounts.router)
app.include_router(loans.router)
app.include_router(users.router)
app.include_router(auth.router)
