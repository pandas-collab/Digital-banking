import sqlite3
import logging
from typing import Dict, List, Any
import json

logging.basicConfig(level=logging.INFO)

class Database:
    def __init__(self, db_path="banking.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self) -> None:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS loan_applications (
                    id TEXT PRIMARY KEY,
                    applicant_name TEXT NOT NULL,
                    amount REAL NOT NULL CHECK(amount > 0),
                    term INTEGER NOT NULL CHECK(term > 0),
                    annual_income REAL NOT NULL CHECK(annual_income > 0),
                    employment_status TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            conn.commit()
            conn.close()
            logging.info("Database initialized successfully")
        except Exception as e:
            logging.error(f"Database initialization failed: {e}")
            raise

    def save_application(self, data: Dict[str, Any]) -> str:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            application_id = f"loan_{int(time.time() * 1000)}"
            cursor.execute('''
                INSERT INTO loan_applications
                (id, applicant_name, amount, term, annual_income, employment_status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                application_id,
                data['applicantName'],
                data['amount'],
                data['term'],
                data['annualIncome'],
                data['employmentStatus']
            ))

            conn.commit()
            conn.close()

            logging.info(f"Application saved: {application_id}")
            return application_id
        except Exception as e:
            logging.error(f"Failed to save application: {e}")
            raise

    def get_applications(self) -> List[Dict[str, Any]]:
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM loan_applications ORDER BY created_at DESC")
            results = [dict(row) for row in cursor.fetchall()]

            conn.close()
            return results
        except Exception as e:
            logging.error(f"Failed to get applications: {e}")
            return []

if __name__ == "__main__":
    db = Database()
    db.init_db()
