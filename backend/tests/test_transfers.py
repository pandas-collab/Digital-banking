import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_transfer():
    payload = {"from_account_id": 1, "to_account_id": 2, "amount": 100.00}
    r = client.post("/transfers", json=payload)
    assert r.status_code == 200
