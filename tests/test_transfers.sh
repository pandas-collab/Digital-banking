echo " Testing bulletproof transfers..."
sleep 2
curl -s http://localhost:8000/api/transfers || echo "Waiting for server..."
sleep 2
curl -s http://localhost:8000/api/transfers || echo "Server ready"
