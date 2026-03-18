import requests
import json

BASE_URL = "http://localhost:8000"

def test_create_policy():
    """Test the POST /api/policies endpoint"""
    policy_data = {
        "plan": "Premium Health Plan",
        "premium": 500.0,
        "coverage": 500000.0,
        "email": "test@example.com"
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/policies",
            json=policy_data,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            result = response.json()
            print(" Policy created successfully:")
            print(json.dumps(result, indent=2))
            return result["data"]["id"]
        else:
            print(f" Failed to create policy: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f" Error creating policy: {e}")
        return None

def test_get_policy(policy_id):
    """Test GET /api/policies/{policy_id} endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/policies/{policy_id}")
        if response.status_code == 200:
            result = response.json()
            print(" Policy retrieved successfully:")
            print(json.dumps(result, indent=2))
        else:
            print(f" Failed to get policy: {response.status_code} - {response.text}")
    except Exception as e:
        print(f" Error getting policy: {e}")

if __name__ == "__main__":
    print("Testing API endpoints...")
    policy_id = test_create_policy()
    if policy_id:
        test_get_policy(policy_id)
