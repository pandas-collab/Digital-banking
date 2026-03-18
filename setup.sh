set -e
cd "$(dirname "$0")"

echo "  Setting up bulletproof loan system..."

# Install dependencies
pip install -r requirements.txt

# Create environment file
if [ ! -f .env ]; then
    cat > .env << EOL
DATABASE_URL=sqlite:///./loans.db
SECRET_KEY=your-secret-key-change-in-production
EOL
fi

# Initialize database
python -c "from loan import Base; from db import engine; Base.metadata.create_all(bind=engine)"

echo " Setup complete! Run 'uvicorn main:app --reload --host 0.0.0.0 --port 8000' to start the server"
echo " Admin dashboard: http://localhost:8000/docs"
exit 0
