cd /workspace

echo "Starting Banking Platform with Enhanced Reliability..."

# Install dependencies in quiet mode
python3 -m pip install --quiet --no-cache-dir fastapi uvicorn sqlite3 > /dev/null 2>&1 || {
    echo "Installing requirements..."
    python3 -m pip install fastapi uvicorn > /dev/null 2>&1
}

# Kill any existing processes
pkill -f "uvicorn" 2>/dev/null || true
pkill -f "python3" 2>/dev/null || true

# Start backend with retry mechanism
(
    cd server
    python3 -u transfer_api.py &
    BACKEND_PID=$!
    echo $BACKEND_PID > /tmp/backend.pid

    # Wait for backend to start
    for i in {1..30}; do
        if curl -s http://localhost:8000/api/transfers/ACC001 > /dev/null 2>&1; then
            echo " Backend started successfully"
            break
        fi
        echo "Backend starting... attempt $i/30"
        sleep 1
    done

    if [ $i -eq 30 ]; then
        echo " Backend failed to start"
        exit 1
    fi
) &

# Simple frontend setup
if [ -d "node_modules" ]; then
    echo " Frontend ready"
else
    echo "Setting up frontend..."
    npm init -y > /dev/null 2>&1
    npm install --quiet --no-save react react-dom > /dev/null 2>&1 || true
fi

echo ""
echo " Banking Platform Started!"
echo " Backend API: http://localhost:8000"
echo " Test accounts: ACC001 ($1000), ACC002 ($500), ACC003 ($2000)"
echo " Daily transfer limit: $1000 per account"
echo ""
echo " To test transfers:"
echo "1. Open browser dev tools"
echo "2. Run: fetch('http://localhost:8000/api/transfers/ACC001')"
echo "3. Try a POST request to test transfers"
