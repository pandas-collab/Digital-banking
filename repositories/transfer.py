from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Tuple
from uuid import UUID
from models.transfer import Transfer

class TransferRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_user_id(self, user_id: UUID, page: int = 0, size: int = 10) -> Tuple[List[Transfer], int]:
        """
        Find transfers for a specific user with pagination
        Returns: (transfers_list, total_pages)
        """
        query = self.db.query(Transfer).filter(Transfer.user_id == user_id)

        total_count = query.with_entities(func.count(Transfer.id)).scalar()
        total_pages = max(1, (total_count + size - 1) // size)

        transfers = (query
                    .order_by(Transfer.created_at.desc())
                    .offset(page * size)
                    .limit(size)
                    .all())

        return transfers, total_pages

    def save(self, transfer: Transfer) -> Transfer:
        """Save a new transfer record"""
        self.db.add(transfer)
        self.db.commit()
        self.db.refresh(transfer)
        return transfer
