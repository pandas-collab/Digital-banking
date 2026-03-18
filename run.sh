set -e

echo "Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

echo "Starting Loan Service API..."
python -m uvicorn api.server:app --host 0.0.0.0 --port 8000 &
PID=$!

sleep 3

echo "Running tests..."
./tests/test_api.sh || {
    echo "Tests failed, stopping server..."
    kill $PID
    exit 1
}

echo "Server started successfully (PID: $PID)"
echo "API available at: http://localhost:8000"
echo "Press Ctrl+C to stop"

trap "kill $PID" EXIT
wait
