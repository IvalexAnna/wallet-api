import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.database import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_wallet(test_db):
    response = client.post("/api/v1/wallets")
    assert response.status_code == 200
    data = response.json()
    assert data["balance"] == 0.0
    assert "id" in data


def test_get_wallet_balance(test_db):
    create_response = client.post("/api/v1/wallets")
    wallet_id = create_response.json()["id"]
    response = client.get(f"/api/v1/wallets/{wallet_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == wallet_id
    assert data["balance"] == 0.0


def test_deposit_operation(test_db):
    create_response = client.post("/api/v1/wallets")
    wallet_id = create_response.json()["id"]
    deposit_data = {"operation_type": "DEPOSIT", "amount": 1000.0}
    response = client.post(f"/api/v1/wallets/{wallet_id}/operation", json=deposit_data)
    assert response.status_code == 200
    data = response.json()
    assert data["operation_type"] == "DEPOSIT"
    assert data["amount"] == 1000.0
    assert data["new_balance"] == 1000.0
    assert data["success"] == True


def test_withdraw_operation(test_db):
    create_response = client.post("/api/v1/wallets")
    wallet_id = create_response.json()["id"]

    deposit_data = {"operation_type": "DEPOSIT", "amount": 1000.0}
    client.post(f"/api/v1/wallets/{wallet_id}/operation", json=deposit_data)

    withdraw_data = {"operation_type": "WITHDRAW", "amount": 500.0}
    response = client.post(f"/api/v1/wallets/{wallet_id}/operation", json=withdraw_data)
    assert response.status_code == 200
    data = response.json()
    assert data["operation_type"] == "WITHDRAW"
    assert data["amount"] == 500.0
    assert data["new_balance"] == 500.0


def test_insufficient_funds(test_db):
    create_response = client.post("/api/v1/wallets")
    wallet_id = create_response.json()["id"]

    withdraw_data = {"operation_type": "WITHDRAW", "amount": 500.0}
    response = client.post(f"/api/v1/wallets/{wallet_id}/operation", json=withdraw_data)
    assert response.status_code == 400
    assert "Insufficient funds" in response.json()["detail"]


def test_operation_nonexistent_wallet(test_db):
    operation_data = {"operation_type": "DEPOSIT", "amount": 100}
    response = client.post(
        "/api/v1/wallets/00000000-0000-0000-0000-000000000000/operation",
        json=operation_data,
    )
    assert response.status_code == 400
    assert "Wallet not found" in response.json()["detail"]


def test_operation_invalid_uuid(test_db):
    operation_data = {"operation_type": "DEPOSIT", "amount": 100}
    response = client.post(
        "/api/v1/wallets/invalid-uuid/operation", json=operation_data
    )
    assert response.status_code == 400


def test_operation_negative_amount(test_db):
    create_response = client.post("/api/v1/wallets")
    wallet_id = create_response.json()["id"]

    operation_data = {"operation_type": "DEPOSIT", "amount": -100}
    response = client.post(
        f"/api/v1/wallets/{wallet_id}/operation", json=operation_data
    )
    assert response.status_code == 422


def test_operation_zero_amount(test_db):
    create_response = client.post("/api/v1/wallets")
    wallet_id = create_response.json()["id"]

    operation_data = {"operation_type": "DEPOSIT", "amount": 0}
    response = client.post(
        f"/api/v1/wallets/{wallet_id}/operation", json=operation_data
    )
    assert response.status_code == 422


def test_operation_invalid_type(test_db):
    create_response = client.post("/api/v1/wallets")
    wallet_id = create_response.json()["id"]

    operation_data = {"operation_type": "INVALID_TYPE", "amount": 100}
    response = client.post(
        f"/api/v1/wallets/{wallet_id}/operation", json=operation_data
    )
    assert response.status_code == 422


def test_health_check(test_db):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_endpoint(test_db):
    response = client.get("/")
    assert response.status_code == 200
    assert "Wallet API is running" in response.json()["message"]
