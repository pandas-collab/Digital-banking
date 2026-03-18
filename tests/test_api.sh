set -e

# Test basic health
echo "Testing health check..."
curl -s "http://localhost:8000/health" | grep -q "healthy" && echo "Health check: OK"

# Test POST /api/loans
echo "Testing loan creation..."
RESPONSE=$(curl -s -X POST "http://localhost:8000/api/loans" \
  -H "Content-Type: application/json" \
  -d '{"amount": 10000.50, "term": 24}')

echo "Response: $RESPONSE"
echo "$RESPONSE" | grep -q '"amount": 10000.5' && echo "POST /api/loans: OK"

# Test validation for negative amount
echo "Testing validation..."
RESPONSE=$(curl -s -X POST "http://localhost:8000/api/loans" \
  -H "Content-Type: application/json" \
  -d '{"amount": -1000, "term": 12}' || true)

echo "$RESPONSE" | grep -q "positive" && echo "Validation check: OK"

echo "All tests completed!"
