set -e
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Starting API server..."
python -m uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload &
echo "Server started on port 8000"
sleep 2
echo "Running tests..."
python test_api.py
