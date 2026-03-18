import pytest
from httpx import AsyncClient
from sqlalchemy import text
import asyncio
from datetime import datetime
from uuid import uuid4

@pytest.mark.asyncio
async def test_create_loan_success(authenticated_client, test_user):
    """Test successful loan creation with auto-approval for small amounts."""
    response = await authenticated_client.post(
        "/api/loans",
        json={"amount": 1000.00, "termMonths": 12}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 1000.00
    assert data["termMonths"] == 12
    assert data["status"] == "APPROVED"  # Auto-approved under $5000
    assert data["userId"] == str(test_user.id)
    assert "id" in data
    assert "createdAt" in data
    assert "approvedAt" in data
    assert data["approvedAt"] is not None

@pytest.mark.asyncio
async def test_create_loan_validation_errors(authenticated_client):
    """Test various validation scenarios."""
    # Negative amount
    response = await authenticated_client.post(
        "/api/loans",
        json={"amount": -1000, "termMonths": 12}
    )
    assert response.status_code == 422

    # Zero amount
    response = await authenticated_client.post(
        "/api/loans",
        json={"amount": 0, "termMonths": 12}
    )
    assert response.status_code == 422

    # Too short term
    response = await authenticated_client.post(
        "/api/loans",
        json={"amount": 1000, "termMonths": 3}
    )
    assert response.status_code == 400

    # Too long term
    response = await authenticated_client.post(
        "/api/loans",
        json={"amount": 1000, "termMonths": 72}
    )
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_create_large_loan_pending(authenticated_client, test_user):
    """Test loan above auto-approval threshold remains pending."""
    response = await authenticated_client.post(
        "/api/loans",
        json={"amount": 6000.00, "termMonths": 24}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "PENDING"  # Not auto-approved
    assert data["approvedAt"] is None

@pytest.mark.asyncio
async def test_get_loans_list(authenticated_client, test_user):
    """Test retrieving user's loans."""
    # Create a loan
    await authenticated_client.post(
        "/api/loans",
        json={"amount": 2000, "termMonths": 6}
    )

    response = await authenticated_client.get("/api/loans")
    assert response.status_code == 200

    loans = response.json()
    assert isinstance(loans, list)
    assert len(loans) >= 1

    # Verify loan structure
    loan = loans[0]
    assert "id" in loan
    assert "userId" in loan
    assert isinstance(loan["amount"], float)
    assert isinstance(loan["termMonths"], int)
    assert loan["status"] in ["PENDING", "APPROVED", "REJECTED", "DISBURSED", "CLOSED"]

@pytest.mark.asyncio
async def test_create_loan_unauthorized(client):
    """Test unauthorized access."""
    response = await client.post(
        "/api/loans",
        json={"amount": 1000, "termMonths": 12}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_loan_status(authenticated_client, test_user):
    """Test retrieving detailed loan status."""
    # Create a loan
    create_response = await authenticated_client.post(
        "/api/loans",
        json={"amount": 1500, "termMonths": 12}
    )
    loan_id = create_response.json()["id"]

    # Get loan status
    response = await authenticated_client.get(f"/api/loans/{loan_id}/status")
    assert response.status_code == 200

    status_data = response.json()
    assert "balance" in status_data
    assert "nextDueDate" in status_data
    assert "status" in status_data
    assert "repaymentSchedule" in status_data
    assert isinstance(status_data["repaymentSchedule"], list)
    assert len(status_data["repaymentSchedule"]) == 12

@pytest.mark.asyncio
async def test_get_loan_status_not_found(authenticated_client, test_user):
    """Test getting status for non-existent loan."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await authenticated_client.get(f"/api/loans/{fake_id}/status")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_get_loan_status_unauthorized(authenticated_client, different_user):
    """Test accessing another user's loan."""
    # Create loan with first user
    create_response = await authenticated_client.post(
        "/api/loans",
        json={"amount": 1000, "termMonths": 12}
    )
    loan_id = create_response.json()["id"]

    # Try to access with different user
    response = await different_user.get(f"/api/loans/{loan_id}/status")
    assert response.status_code == 403
