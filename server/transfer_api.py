import os
import time
import logging
from datetime import datetime, date
from typing import List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import sqlite3
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TransferRequest(BaseModel):
    from_account: str = Field(..., min_length=1)
    to_account: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    description: str = Field("", max_length=200)

class TransferResponse(BaseModel):
    success: bool
    transaction_id: str
    message: str

class DailyLimitExceeded(Exception):
    pass

class InsufficientFunds(Exception):
    pass

class TransferService:
    def __init__(self):
        self.conn = sqlite3.connect('banking.db', check_same_thread=False)
        self.init_database()

    def init_database(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id TEXT PRIMARY KEY,
                balance REAL NOT NULL DEFAULT 0
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transfers (
                id TEXT PRIMARY KEY,
                from_account TEXT NOT NULL,
                to_account TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                timestamp TEXT NOT NULL
            )
        ''')
        self.conn.commit()

        # Add test data
        cursor.execute('SELECT COUNT(*) FROM accounts')
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO accounts (id, balance) VALUES (?, ?)', ('ACC001', 1000))
            cursor.execute('INSERT INTO accounts (id, balance) VALUES (?, ?)', ('ACC002', 500))
            cursor.execute('INSERT INTO accounts (id, balance) VALUES (?, ?)', ('ACC003', 2000))
            self.conn.commit()

    def check_daily_limit(self, account: str) -> bool:
        cursor = self.conn.cursor()
        today = str(date.today())
        cursor.execute('''
            SELECT SUM(amount) FROM transfers
            WHERE from_account = ? AND date(timestamp) = ?
        ''', (account, today))
        total = cursor.fetchone()[0] or 0
        return total < 1000

    def transfer_funds(self, request: TransferRequest) -> TransferResponse:
        try:
            # Check daily limit
            if not self.check_daily_limit(request.from_account):
                raise DailyLimitExceeded("Daily transfer limit exceeded")

            # Check balances
            cursor = self.conn.cursor()
            cursor.execute('SELECT balance FROM accounts WHERE id = ?', (request.from_account,))
            from_balance = cursor.fetchone()
            if not from_balance or from_balance[0] < request.amount:
                raise InsufficientFunds("Insufficient funds")

            cursor.execute('SELECT balance FROM accounts WHERE id = ?', (request.to_account,))
            to_balance = cursor.fetchone()
            if not to_balance:
                raise HTTPException(404, "Destination account not found")

            # Perform transfer
            transaction_id = f"TXN-{datetime.now().strftime('%Y%m%d-%H%M%S-%f')}"

            # Update balances
            cursor.execute('UPDATE accounts SET balance = balance - ? WHERE id = ?',
                         (request.amount, request.from_account))
            cursor.execute('UPDATE accounts SET balance = balance + ? WHERE id = ?',
                         (request.amount, request.to_account))

            # Record transaction
            cursor.execute('''
                INSERT INTO transfers (id, from_account, to_account, amount, description, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (transaction_id, request.from_account, request.to_account,
                  request.amount, request.description, str(datetime.now())))

            self.conn.commit()
            logger.info(f"Transfer completed: {transaction_id}")
            return TransferResponse(success=True, transaction_id=transaction_id,
                                  message="Transfer completed successfully")

        except DailyLimitExceeded as e:
            self.conn.rollback()
            raise HTTPException(400, str(e))
        except InsufficientFunds as e:
            self.conn.rollback()
            raise HTTPException(400, str(e))
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Transfer failed: {str(e)}")
            raise HTTPException(500, f"Transfer failed: {str(e)}")

    def get_transfer_history(self, account: str) -> List[Dict]:
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT * FROM transfers
                WHERE from_account = ? OR to_account = ?
                ORDER BY timestamp DESC
                LIMIT 50
            ''', (account, account))

            columns = ['id', 'from_account', 'to_account', 'amount', 'description', 'timestamp']
            transfers = []
            for row in cursor.fetchall():
                transfers.append(dict(zip(columns, row)))
            return transfers

        except Exception as e:
            logger.error(f"Failed to get history: {str(e)}")
            raise HTTPException(500, "Failed to retrieve transfer history")

service = TransferService()
app = FastAPI()

@app.post("/api/transfers", response_model=TransferResponse)
async def create_transfer(request: TransferRequest):
    return service.transfer_funds(request)

@app.get("/api/transfers/{account}")
async def get_transfers(account: str):
    return service.get_transfer_history(account)

@app.get("/api/accounts/{account}")
async def get_account(account: str):
    cursor = service.conn.cursor()
    cursor.execute('SELECT * FROM accounts WHERE id = ?', (account,))
    result = cursor.fetchone()
    if not result:
        raise HTTPException(404, "Account not found")
    return {"id": result[0], "balance": result[1]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
