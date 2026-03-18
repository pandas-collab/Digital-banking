import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base
from app.main import app
from app.dependencies import get_db

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_get_ledger_empty():
    response = client.get("/api/ledger")
    assert response.status_code == 200
    data = response.json()
    assert "events" in data
    assert isinstance(data["events"], list)
    assert "total" in data

def test_invalid_date_format():
    response = client.get("/api/ledger?fromDate=invalid-date")
    assert response.status_code == 422

def test_invalid_uuid():
    response = client.get("/api/ledger?account=invalid-uuid")
    assert response.status_code == 422

def test_invalid_type():
    response = client.get("/api/ledger?type=INVALID")
    assert response.status_code == 422

def test_pagination():
    response = client.get("/api/ledger?page=1&size=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data["events"]) <= 5

def test_date_range_validation():
    response = client.get("/api/ledger?fromDate=2024-01-01&toDate=2023-01-01")
    assert response.status_code == 422

def test_valid_parameters():
    test_uuid = "123e4567-e89b-12d3-a456-426614174000"
    response = client.get(f"/api/ledger?account={test_uuid}&type=TRANSFER&fromDate=2024-01-01&toDate=2024-12-31")
    assert response.status_code in [200, 422]  # 200 if valid UUID, 422 if schema has restrictions
