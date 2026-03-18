set -e

# Database initialization script
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-cashflow}"
DB_USER="${DB_USER:-postgres}"
DB_PASS="${DB_PASS:-postgres}"

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."
while ! pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  sleep 1
done

# Create database if it doesn't exist
PGPASSWORD=$DB_PASS psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -c "SELECT 'CREATE DATABASE $DB_NAME' WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = '$DB_NAME')\gexec"

# Apply migrations
export PGPASSWORD=$DB_PASS
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f ../internal/migrations/001_create_cashflow_ledger.sql

echo "Database initialized successfully!"
echo "Database: $DB_NAME"
echo "Table: cashflow_ledger"
echo "View: cashflow_ledger_balance"
