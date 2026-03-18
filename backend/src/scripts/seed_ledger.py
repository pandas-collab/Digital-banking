"""
Seed script to populate sample ledger data for testing.
"""

import asyncio
import os
from datetime import datetime, timedelta
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.models.ledger import Ledger
from src.schemas.ledger import LedgerCreate
from src.services.ledger_service import LedgerService

# Database connection
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/banking"
)

async def create_sample_data():
    """Create sample ledger entries."""
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        # Clear existing data
        await session.execute(select(Ledger).delete())
        await session.commit()

        # Sample transfers
        transfers = [
            {
                "transfer_id": 1001,
                "amount": Decimal("150.75"),
                "events": ["transfer_initiated", "transfer_completed"]
            },
            {
                "transfer_id": 1002,
                "amount": Decimal("2500.00"),
                "events": ["transfer_initiated", "transfer_completed"]
            },
            {
                "transfer_id": 1003,
                "amount": Decimal("500.00"),
                "events": ["transfer_initiated", "transfer_failed"]
            }
        ]

        base_time = datetime.utcnow()

        for transfer in transfers:
            from_balance_before = Decimal("10000.00")
            from_balance_after = from_balance_before - transfer["amount"]
            to_balance_before = Decimal("5000.00")
            to_balance_after = to_balance_before + transfer["amount"]

            for idx, event in enumerate(transfer["events"]):
                # Failed transfer logic
                if event == "transfer_failed":
                    from_balance_after = from_balance_before
                    to_balance_after = to_balance_before

                entry_data = LedgerCreate(
                    event_type=event,
                    transfer_id=transfer["transfer_id"],
                    from_account_id=1,
                    to_account_id=2,
                    amount=transfer["amount"],
                    from_balance_before=from_balance_before,
                    from_balance_after=from_balance_after,
                    to_balance_before=to_balance_before,
                    to_balance_after=to_balance_after,
                    description=f"Sample {event} for transfer {transfer['transfer_id']}",
                    audit_data={
                        "request_id": str(uuid4()),
                        "user_agent": "ledger-seed-script/1.0",
                        "ip_address": "127.0.0.1",
                        "user_id": 1,
                        "session_id": "seed-session-001",
                        "timestamp": datetime.utcnow().isoformat(),
                        "transfer_metadata": {
                            "original_amount": float(transfer["amount"]),
                            "transfer_sequence": idx + 1,
                            "event_index": idx
                        }
                    }
                )

                await LedgerService.create_entry(session, entry_data)

                # Add time offset for ordered events
                base_time += timedelta(seconds=1)

        # Create inter-account transfers
        multi_transfers = [
            {
                "from": 1,
                "to": 3,
                "amount": Decimal("750.00"),
                "events": ["transfer_initiated", "transfer_completed"]
            },
            {
                "from": 3,
                "to": 2,
                "amount": Decimal("300.50"),
                "events": ["transfer_initiated", "transfer_completed"]
            }
        ]

        for mtransfer in multi_transfers:
            from_balance_before = Decimal("8000.00")
            from_balance_after = from_balance_before - mtransfer["amount"]
            to_balance_before = Decimal("3000.00")
            to_balance_after = to_balance_before + mtransfer["amount"]

            for event in mtransfer["events"]:
                entry_data = LedgerCreate(
                    event_type=event,
                    transfer_id=int(f"200{len(os.urandom(4).hex())[:3]}"),
                    from_account_id=mtransfer["from"],
                    to_account_id=mtransfer["to"],
                    amount=mtransfer["amount"],
                    from_balance_before=from_balance_before,
                    from_balance_after=from_balance_after,
                    to_balance_before=to_balance_before,
                    to_balance_after=to_balance_after,
                    description=f"Multi-account {event}",
                    audit_data={
                        "request_id": str(uuid4()),
                        "user_agent": "multi-transfer-seed",
                        "ip_address": "192.168.1.100",
                        "debug": True
                    }
                )

                await LedgerService.create_entry(session, entry_data)

    await engine.dispose()
    print(" Ledger seed data created successfully!")

if __name__ == "__main__":
    asyncio.run(create_sample_data())
