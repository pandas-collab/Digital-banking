set -e

echo " Starting verification of GET /api/transfers endpoint..."

# Install dependencies
echo " Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1 || true

# Create test database
echo " Initializing database..."
python -c "from api.database import Base, engine; Base.metadata.create_all(engine)" 2>/dev/null || echo "Database may already exist"

# Test endpoint
echo " Testing endpoint..."

# Test without auth
echo " Test 1: No authentication"
curl -s -X GET "http://localhost:8000/api/transfers" | grep -q "Missing authentication token" && echo " No auth test passed" || echo " No auth test failed"

# Start server for authenticated tests
echo " Starting FastAPI server..."
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload > /dev/null 2>&1 &
SERVER_PID=$!

sleep 3

# Create test data
python -c "
import requests
import uuid
user_id = 'a1b2c3d4-e5f6-7890-abcd-1234567890ab'
for i in range(3):
    requests.post('http://localhost:8000/api/transfers',
        json={'fromAccountId': str(uuid.uuid4()), 'toAccountId': str(uuid.uuid4()), 'amount': 100.00},
        headers={'Authorization': 'Bearer ' + user_id}
    )
" 2>/dev/null || echo "Failed to create test data"

# Test authenticated requests
echo " Test 2: Authenticated request"
RESPONSE=$(curl -s -X GET "http://localhost:8000/api/transfers" \
  -H "Authorization: Bearer a1b2c3d4-e5f6-7890-abcd-1234567890ab")
echo "Response: $RESPONSE"
echo "$RESPONSE" | jq '. | has("content") and has("totalPages")' | grep -q "true" && echo " Auth test passed" || echo " Auth test failed"

echo " Test 3: Pagination"
RESPONSE=$(curl -s -X GET "http://localhost:8000/api/transfers?page=0&size=2" \
  -H "Authorization: Bearer a1b2c3d4-e5f6-7890-abcd-1234567890ab")
echo "$RESPONSE" | jq '.'

# Kill server
kill $SERVER_PID 2>/dev/null || true

echo " Verification complete!"
