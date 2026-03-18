from sqlalchemy.orm import Session
from sqlalchemy import and_, between
from uuid import UUID
from typing import Optional, List, Tuple
from app.models.ledger import Ledger
import logging

logger = logging.getLogger(__name__)

class LedgerRepository:
    def __init__(self, db: Session):
        self.db = db

    def query_ledger(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        account_id: Optional[str] = None,
        event_type: Optional[str] = None,
        page: int = 1,
        size: int = 10
    ) -> Tuple[List[Ledger], int]:
        try:
            query = self.db.query(Ledger)

            # Apply filters
            if from_date and to_date:
                from datetime import datetime, timezone
                from dateutil import parser
                start_date = parser.parse(from_date).replace(tzinfo=timezone.utc)
                end_date = parser.parse(to_date).replace(tzinfo=timezone.utc)
                query = query.filter(
                    and_(
                        Ledger.ts >= start_date,
                        Ledger.ts <= end_date
                    )
                )
            elif from_date:
                from datetime import datetime, timezone
                from dateutil import parser
                start_date = parser.parse(from_date).replace(tzinfo=timezone.utc)
                query = query.filter(Ledger.ts >= start_date)
            elif to_date:
                from datetime import datetime, timezone
                from dateutil import parser
                end_date = parser.parse(to_date).replace(tzinfo=timezone.utc)
                query = query.filter(Ledger.ts <= end_date)

            if account_id:
                query = query.filter(Ledger.account_id == UUID(account_id))

            if event_type:
                query = query.filter(Ledger.type == event_type)

            total = query.count()

            # Apply pagination
            offset = (page - 1) * size
            results = query.offset(offset).limit(size).all()

            logger.info(
                "Querying ledger: account=%s type=%s from=%s to=%s limit=%s offset=%s",
                account_id,
                event_type,
                from_date,
                to_date,
                size,
                offset
            )

            return results, total

        except Exception as e:
            logger.error(f"Database query failed: {str(e)}")
            raise
