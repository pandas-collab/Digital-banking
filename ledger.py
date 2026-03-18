import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO)

class Ledger:
    def __init__(self):
        self.transactions = []

    def record_transaction(self, transaction: Dict):
        try:
            if not transaction.get('id'):
                raise ValueError("Transaction ID required")
            if not transaction.get('amount') or transaction['amount'] <= 0:
                raise ValueError("Valid amount required")

            transaction['timestamp'] = __import__('time').time()
            self.transactions.append(transaction)

            logging.info(f"Transaction recorded: {transaction['id']}")
            return True
        except Exception as e:
            logging.error(f"Failed to record transaction: {e}")
            return False

    def get_balance(self, account_id: str) -> float:
        balance = 0
        for tx in self.transactions:
            if tx.get('from') == account_id:
                balance -= tx.get('amount', 0)
            if tx.get('to') == account_id:
                balance += tx.get('amount', 0)
        return balance

    def get_transaction_history(self, account_id: str = None) -> List[Dict]:
        if account_id:
            return [tx for tx in self.transactions
                   if tx.get('from') == account_id or tx.get('to') == account_id]
        return self.transactions
