import requests
import json

def test_create_loan():
    """Test creating a loan through the API"""
    url = "http://localhost:8000/api/loans"
    data = {
        "applicant_name": "John Doe",
        "email": "john.doe@example.com",
        "amount": 5000.0,
        "interest_rate": 5.5,
        "term_months": 24
    }

    try:
        response = requests.post(url, json=data)
        print(f"Create loan response: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return response.json()
    except Exception as e:
        print(f"Error creating loan: {e}")
        return None

def test_list_loans():
    """Test listing all loans"""
    url = "http://localhost:8000/api/loans"

    try:
        response = requests.get(url)
        print(f"List loans response: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error listing loans: {e}")

if __name__ == "__main__":
    # Wait a moment for the server to start
    import time
    time.sleep(2)

    test_create_loan()
    test_list_loans()
