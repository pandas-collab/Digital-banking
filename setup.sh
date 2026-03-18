echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting backend API..."
cd backend
python -c "
import uvicorn
uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
" &
API_PID=$!

echo "Waiting for backend to start..."
sleep 3

echo "Starting frontend..."
cd ../frontend
npm install
npm start &
FRONTEND_PID=$!

echo "Services started!"
echo "Backend API: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"

trap "kill $API_PID $FRONTEND_PID" EXIT
wait
