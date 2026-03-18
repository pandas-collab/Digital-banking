"""Comprehensive test suite for ledger functionality."""

import asyncio
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.ledger import Ledger
from src.schemas.ledger import LedgerCreate
from src.services.ledger_service import LedgerService

@pytest.fixture
async def sample_ledger_data() -> Dict:
    """Provide sample ledger data for testing."""
    return {
        "event_type": "transfer_initiated",
        "transfer_id": 1,
        "from_account_id": 1,
        "to_account_id": 2,
        "amount": Decimal("100.50"),
        "from_balance_before": Decimal("1000.00"),
        "from_balance_after": Decimal("899.50"),
        "to_balance_before": Decimal("500.00"),
        "to_balance_after": Decimal("600.50"),
        "description": "Test transfer",
        "audit_data": {
            "request_id": "test-001",
            "user_agent": "test-agent",
            "ip_address": "127.0.0.1",
            "extra_metadata": {"test": True}
        }
    }

@pytest.mark.asyncio
async def test_create_ledger_entry(test_db: AsyncSession, sample_ledger_data: Dict):
    """Test creating a ledger entry."""
    entry_data = LedgerCreate(**sample_ledger_data)
    result = await LedgerService.create_entry(test_db, entry_data)

    assert result.amount == sample_ledger_data["amount"]
    assert result.event_type == "transfer_initiated"
    assert result.audit_data["request_id"] == "test-001"

    # Verify in database
    stmt = select(Ledger).where(Ledger.id == result.id)
    db_result = await test_db.execute(stmt)
    db_entry = db_result.scalar()

    assert db_entry is not None
    assert db_entry.amount == sample_ledger_data["amount"]

@pytest.mark.asyncio
async def test_get_user_ledger(test_db: AsyncSession, sample_ledger_data: Dict):
    """Test retrieving user ledger entries."""
    # Create multiple entries
    entries = [
        LedgerCreate(**sample_ledger_data),
        LedgerCreate(
            **{
                **sample_ledger_data,
                "transfer_id": 2,
                "to_account_id": 3,
                "amount": Decimal("50.25"),
                "event_type": "transfer_completed"
            }
        )
    ]

    for entry in entries:
        await LedgerService.create_entry(test_db, entry)

    # Get ledger for user 1
    result = await LedgerService.get_user_ledger(test_db, 1, page=1, per_page=10)

    assert result.total >= 2
    assert all(
        entry.from_account_id == 1 or entry.to_account_id == 1
        for entry in result.items
    )

@pytest.mark.asyncio
async def test_pagination(test_db: AsyncSession, sample_ledger_data: Dict):
    """Test pagination functionality."""
    # Create 30 entries
    for i in range(30):
        data = {
            **sample_ledger_data,
            "transfer_id": i + 10,
            "amount": Decimal("10.00")
        }
        await LedgerService.create_entry(test_db, LedgerCreate(**data))

    # Test page 1
    page1 = await LedgerService.get_user_ledger(test_db, 1, page=1, per_page=10)
    assert len(page1.items) == 10
    assert page1.page == 1
    assert page1.per_page == 10

    # Test page 2
    page2 = await LedgerService.get_user_ledger(test_db, 1, page=2, per_page=10)
    assert len(page2.items) == 10
    assert page2.page == 2

    # Test custom per_page
    custom_page = await LedgerService.get_user_ledger(test_db, 1, page=1, per_page=15)
    assert len(custom_page.items) == 15

@pytest.mark.asyncio
async def test_get_transfer_ledger(test_db: AsyncSession, sample_ledger_data: Dict):
    """Test retrieving ledger entries for a specific transfer."""
    # Create entries for same transfer
    events = [
        "transfer_initiated",
        "transfer_completed"
    ]

    for event in events:
        data = {
            **sample_ledger_data,
            "event_type": event
        }
        await LedgerService.create_entry(test_db, LedgerCreate(**data))

    # Get ledger for transfer
    entries = await LedgerService.get_transfer_ledger(test_db, 1)

    assert len(entries) == 2
    assert entries[0].event_type == "transfer_initiated"
    assert entries[1].event_type == "transfer_completed"

@pytest.mark.asyncio
async def test_ledger_validation():
    """Test schema validation."""
    # Test invalid event type
    with pytest.raises(ValueError):
        LedgerCreate(
            event_type="invalid_type",
            transfer_id=1,
            from_account_id=1,
            to_account_id=2,
            amount=Decimal("100"),
            from_balance_before=Decimal("1000"),
            from_balance_after=Decimal("900"),
            to_balance_before=Decimal("500"),
            to_balance_after=Decimal("600")
        )

    # Test invalid numeric precision
    with pytest.raises(ValueError):
        LedgerCreate(
            event_type="transfer_initiated",
            transfer_id=1,
            from_account_id=1,
            to_account_id=2,
            amount=Decimal("100.999"),  # More than 2 decimal places
            from_balance_before=Decimal("1000"),
            from_balance_after=Decimal("900"),
            to_balance_before=Decimal("500"),
            to_balance_after=Decimal("600")
        )

@pytest.mark.asyncio
async def test_api_endpoints(test_client: AsyncClient, test_db: AsyncSession):
    """Test API endpoints."""
    # This test assumes test fixtures provide valid auth token
    response = await test_client.get("/api/v1/ledger")
    assert response.status_code == 200

    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "per_page" in data

@pytest.mark.asyncio
async def test_immutability(test_db: AsyncSession, sample_ledger_data: Dict):
    """Test that ledger entries are immutable."""
    entry = await LedgerService.create_entry(test_db, LedgerCreate(**sample_ledger_data))

    # Try to modify directly via SQL
    entry.amount = Decimal("999.99")
    test_db.add(entry)
    await test_db.commit()

    # Verify original entry unchanged
    stmt = select(Ledger).where(Ledger.id == entry.id)
    result = await test_db.execute(stmt)
    fresh_entry = result.scalar()

    assert fresh_entry.amount == sample_ledger_data["amount"]

@pytest.mark.asyncio
async def test_audit_data_jsonb(test_db: AsyncSession):
    """Test JSONB audit data storage."""
    audit_data = {
        "request_id": "req-123",
        "user_agent": "Mozilla/5.0...",
        "ip_address": "192.168.1.1",
        "nested": {"data": {"works": True}}
    }

    entry_data = LedgerCreate(
        event_type="transfer_initiated",
        transfer_id=999,
        from_account_id=1,
        to_account_id=2,
        amount=Decimal("50.00"),
        from_balance_before=Decimal("100.00"),
        from_balance_after=Decimal("50.00"),
        to_balance_before=Decimal("0.00"),
        to_balance_after=Decimal("50.00"),
        audit_data=audit_data
    )

    result = await LedgerService.create_entry(test_db, entry_data)
    assert result.audit_data == audit_data
    assert result.audit_data["nested"]["data"]["works"] is True
