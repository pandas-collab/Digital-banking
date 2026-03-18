
echo " Setting up ledger table..."

# Run alembic migration
cd backend
alembic upgrade head

# Seed sample data
python -m src.scripts.seed_ledger

echo " Ledger setup complete!"
