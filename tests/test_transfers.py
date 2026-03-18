import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.database import Base
from main import app
from models.transfer import Transfer
from uuid import uuid4

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override dependencies for testing
app.dependency_overrides[override_get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user_id():
    return str(uuid4())

@pytest.fixture
def create_test_transfers(test_user_id):
    def _create_transfers(count: int):
        db = TestingSessionLocal()
        transfers = []
        for i in range(count):
            transfer = Transfer(
                id=str(uuid4()),
                user_id=test_user_id,
                from_account_id=str(uuid4()),
                to_account_id=str(uuid4()),
                amount=100.00 + i
            )
            transfers.append(transfer)
        db.add_all(transfers)
        db.commit()
        db.close()
    return _create_transfers

class TestGetTransfers:
    def test_get_transfers_no_auth(self, client):
        response = client.get("/api/transfers")
        assert response.status_code == 401

    def test_get_transfers_success(self, client, test_user_id, create_test_transfers):
        create_test_transfers(5)

        response = client.get(
            "/api/transfers",
            headers={"Authorization": f"Bearer {test_user_id}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "content" in data
        assert "totalPages" in data
        assert len(data["content"]) == 5
        assert data["totalPages"] == 1

    def test_get_transfers_pagination(self, client, test_user_id, create_test_transfers):
        create_test_transfers(15)

        # First page
        response = client.get(
            "/api/transfers?page=0&size=10",
            headers={"Authorization": f"Bearer {test_user_id}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["content"]) == 10
        assert data["totalPages"] == 2

        # Second page
        response = client.get(
            "/api/transfers?page=1&size=10",
            headers={"Authorization": f"Bearer {test_user_id}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["content"]) == 5
        assert data["totalPages"] == 2

    def test_get_transfers_empty(self, client, test_user_id):
        response = client.get(
            "/api/transfers",
            headers={"Authorization": f"Bearer {test_user_id}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["content"] == []
        assert data["totalPages"] == 0

    def test_get_transfers_invalid_page(self, client, test_user_id):
        response = client.get(
            "/api/transfers?page=-1&size=10",
            headers={"Authorization": f"Bearer {test_user_id}"}
        )
        assert response.status_code == 400

    def test_get_transfers_invalid_size(self, client, test_user_id):
        response = client.get(
            "/api/transfers?page=0&size=0",
            headers={"Authorization": f"Bearer {test_user_id}"}
        )
        assert response.status_code == 400

        response = client.get(
            "/api/transfers?page=0&size=101",
            headers={"Authorization": f"Bearer {test_user_id}"}
        )
        assert response.status_code == 400

    def test_get_transfers_single_result(self, client, test_user_id, create_test_transfers):
        create_test_transfers(1)

        response = client.get(
            "/api/transfers?page=0&size=1",
            headers={"Authorization": f"Bearer {test_user_id}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["content"]) == 1
        assert data["totalPages"] == 1

        transfer = data["content"][0]
        assert "transferId" in transfer
        assert "fromAccountId" in transfer
        assert "toAccountId" in transfer
        assert "amount" in transfer
        assert "createdAt" in transfer
        assert float(transfer["amount"]) == 100.00

    def test_user_isolation(self, client, test_user_id, create_test_transfers):
        other_user_id = str(uuid4())
        create_test_transfers(3)  # Create transfers for test_user_id

        # Check other user has no transfers
        response = client.get(
            "/api/transfers",
            headers={"Authorization": f"Bearer {other_user_id}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["content"]) == 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
