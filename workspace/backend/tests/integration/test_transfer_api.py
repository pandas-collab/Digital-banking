import pytest
import uuid
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database import get_db_async, Account, User

@pytest.mark.asyncio
async def test_create_transfer_success(test_client: AsyncClient):
    """Test successful transfer creation."""
    async with get_db_async() as db:
        # Create test users
        user1 = User(email="test1@example.com")
        user2 = User(email="test2@example.com")
        db.add_all([user1, user2])
        await db.flush()

        # Create test accounts
        acc1 = Account(user_id=user1.id, balance=1000.00)
        acc2 = Account(user_id=user2.id, balance=500.00)
        db.add_all([acc1, acc2])
        await db.commit()

        from_account_id = str(acc1.id)
        to_account_id = str(acc2.id)

    payload = {
        "fromAccount": from_account_id,
        "toAccount": to_account_id,
        "amount": 100.00
    }

    response = await test_client.post("/api/transfers", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["fromAccount"] == from_account_id
    assert data["toAccount"] == to_account_id
    assert data["amount"] == 100.00
    assert data["status"] == "COMPLETED"
    assert "createdAt" in data
    assert "id" in data

@pytest.mark.asyncio
async def test_create_transfer_invalid_uuid(test_client: AsyncClient):
    """Test transfer with invalid UUID format."""
    payload = {
        "fromAccount": "invalid-uuid",
        "toAccount": "550e8400-e29b-41d4-a716-446655440000",
        "amount": 100.00
    }

    response = await test_client.post("/api/transfers", json=payload)

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_transfer_account_not_found(test_client: AsyncClient):
    """Test transfer with non-existent account."""
    payload = {
        "fromAccount": "550e8400-e29b-41d4-a716-446655440000",
        "toAccount": "550e8400-e29b-41d4-a716-446655440001",
        "amount": 100.00
    }

    response = await test_client.post("/api/transfers", json=payload)

    assert response.status_code == 404

@pytest.mark.asyncio
async def test_create_transfer_insufficient_funds(test_client: AsyncClient):
    """Test transfer with insufficient funds."""
    async with get_db_async() as db:
        user1 = User(email="test3@example.com")
        user2 = User(email="test4@example.com")
        db.add_all([user1, user2])
        await db.flush()

        acc1 = Account(user_id=user1.id, balance=50.00)
        acc2 = Account(user_id=user2.id, balance=500.00)
        db.add_all([acc1, acc2])
        await db.commit()

        from_account_id = str(acc1.id)
        to_account_id = str(acc2.id)

    payload = {
        "fromAccount": from_account_id,
        "toAccount": to_account_id,
        "amount": 100.00
    }

    response = await test_client.post("/api/transfers", json=payload)

    assert response.status_code == 409
    assert "Insufficient funds" in response.json()["detail"]

@pytest.mark.asyncio
async def test_create_transfer_daily_limit_exceeded(test_client: AsyncClient):
    """Test transfer exceeding daily limit."""
    async with get_db_async() as db:
        user1 = User(email="test5@example.com")
        user2 = User(email="test6@example.com")
        db.add_all([user1, user2])
        await db.flush()

        acc1 = Account(user_id=user1.id, balance=600000.00)
        acc2 = Account(user_id=user2.id, balance=500.00)
        db.add_all([acc1, acc2])
        await db.commit()

        from_account_id = str(acc1.id)
        to_account_id = str(acc2.id)

    # First transfer
    payload = {
        "fromAccount": from_account_id,
        "toAccount": to_account_id,
        "amount": 400000.00
    }

    response1 = await test_client.post("/api/transfers", json=payload)
    assert response1.status_code == 201

    # Second transfer that exceeds limit
    payload2 = {
        "fromAccount": from_account_id,
        "toAccount": to_account_id,
        "amount": 200000.00
    }

    response2 = await test_client.post("/api/transfers", json=payload2)
    assert response2.status_code == 409
    assert "Daily transfer limit exceeded" in response2.json()["detail"]

@pytest.mark.asyncio
async def test_create_transfer_self_transfer(test_client: AsyncClient):
    """Test transfer to same account."""
    async with get_db_async() as db:
        user1 = User(email="test7@example.com")
        db.add(user1)
        await db.flush()

        acc1 = Account(user_id=user1.id, balance=1000.00)
        db.add(acc1)
        await db.commit()

        account_id = str(acc1.id)

    payload = {
        "fromAccount": account_id,
        "toAccount": account_id,
        "amount": 100.00
    }

    response = await test_client.post("/api/transfers", json=payload)

    assert response.status_code == 422
    assert "Cannot transfer to the same account" in response.json()["detail"]
