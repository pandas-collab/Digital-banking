import pytest
import json
from services.loan-service.app import create_app

@pytest.fixture
def app():
    app = create_app('testing')
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def headers():
    return {
        'Authorization': 'Bearer test-token',
        'Content-Type': 'application/json'
    }

def test_create_loan_application_success(client, headers):
    data = {
        "amount": 10000,
        "term_months": 24,
        "purpose": "debt_consolidation",
        "annual_income": 60000,
        "employment_status": "full_time"
    }

    response = client.post('/api/loans',
                          data=json.dumps(data),
                          headers=headers)

    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert response_data['amount'] == 10000
    assert response_data['status'] == 'under_review'

def test_create_loan_application_missing_field(client, headers):
    data = {
        "amount": 10000,
        "term_months": 24,
        "purpose": "debt_consolidation"
        # Missing annual_income and employment_status
    }

    response = client.post('/api/loans',
                          data=json.dumps(data),
                          headers=headers)

    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert 'validation_error' in response_data

def test_get_user_loans(client, headers):
    # First create an application
    data = {
        "amount": 15000,
        "term_months": 36,
        "purpose": "home_improvement",
        "annual_income": 80000,
        "employment_status": "full_time"
    }

    client.post('/api/loans', data=json.dumps(data), headers=headers)

    # Then get user loans
    response = client.get('/api/loans', headers=headers)

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert len(response_data) >= 1
    assert response_data[0]['purpose'] == 'home_improvement'
