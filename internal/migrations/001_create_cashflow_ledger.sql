-- 001_create_cashflow_ledger.sql
-- Immutable cash-flow ledger table with JSONB audit fields

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create cashflow_ledger table with immutable design
CREATE TABLE IF NOT EXISTS cashflow_ledger (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    transaction_id UUID NOT NULL,
    account_id VARCHAR(255) NOT NULL,
    amount DECIMAL(15,2) NOT NULL CHECK (amount != 0),
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    transaction_type VARCHAR(50) NOT NULL CHECK (transaction_type IN ('CREDIT', 'DEBIT', 'TRANSFER', 'ADJUSTMENT')),
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'COMPLETED', 'FAILED', 'CANCELLED')),

    -- JSONB fields for extensible audit data
    metadata JSONB NOT NULL DEFAULT '{}',
    audit_trail JSONB NOT NULL DEFAULT '[]',

    -- Immutable bookkeeping columns
    reference_id VARCHAR(255) UNIQUE,
    ledger_sequence BIGSERIAL NOT NULL,

    -- Immutable metadata
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_by VARCHAR(255),

    -- Make the table append-only by removing UPDATE/DELETE triggers
    -- These will be enforced via RLS policies and triggers
    CONSTRAINT cashflow_ledger_positive_sequence CHECK (ledger_sequence > 0)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_cashflow_ledger_account ON cashflow_ledger(account_id);
CREATE INDEX IF NOT EXISTS idx_cashflow_ledger_transaction ON cashflow_ledger(transaction_id);
CREATE INDEX IF NOT EXISTS idx_cashflow_ledger_created_at ON cashflow_ledger(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_cashflow_ledger_reference ON cashflow_ledger(reference_id) WHERE reference_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_cashflow_ledger_metadata ON cashflow_ledger USING GIN(metadata);
CREATE INDEX IF NOT EXISTS idx_cashflow_ledger_audit_trail ON cashflow_ledger USING GIN(audit_trail);

-- Unique constraint to prevent duplicate transactions
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_transaction_account ON cashflow_ledger(transaction_id, account_id);

-- Function to reject direct updates
CREATE OR REPLACE FUNCTION prevent_direct_update()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Ledger entries are immutable and cannot be modified';
END;
$$ LANGUAGE plpgsql;

-- Function to prevent direct deletion
CREATE OR REPLACE FUNCTION prevent_direct_delete()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Ledger entries are immutable and cannot be deleted';
END;
$$ LANGUAGE plpgsql;

-- Triggers to enforce immutability
CREATE TRIGGER prevent_update_on_ledger
    BEFORE UPDATE ON cashflow_ledger
    FOR EACH ROW
    EXECUTE FUNCTION prevent_direct_update();

CREATE TRIGGER prevent_delete_on_ledger
    BEFORE DELETE ON cashflow_ledger
    FOR EACH ROW
    EXECUTE FUNCTION prevent_direct_delete();

-- Function to append to audit trail instead of overwriting
CREATE OR REPLACE FUNCTION append_audit_event()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        NEW.audit_trail = jsonb_build_array(
            jsonb_build_object(
                'event', 'CREATE',
                'timestamp', NOW(),
                'user', COALESCE(NEW.created_by, 'system'),
                'details', NEW.metadata
            )
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to manage audit trail
CREATE TRIGGER manage_audit_trail
    BEFORE INSERT ON cashflow_ledger
    FOR EACH ROW
    EXECUTE FUNCTION append_audit_event();

-- Views for convenience
CREATE OR REPLACE VIEW cashflow_ledger_balance AS
SELECT
    account_id,
    SUM(CASE
        WHEN transaction_type = 'CREDIT' THEN amount
        WHEN transaction_type = 'TRANSFER' AND metadata->>'to_account' = account_id THEN amount
        ELSE -amount
    END) as balance
FROM cashflow_ledger
WHERE status = 'COMPLETED'
GROUP BY account_id;

-- Aggregation function for running totals
CREATE OR REPLACE FUNCTION get_account_balance(account_id_param VARCHAR)
RETURNS DECIMAL(15,2) AS $$
DECLARE
    balance DECIMAL(15,2);
BEGIN
    SELECT COALESCE(SUM(CASE
        WHEN transaction_type = 'CREDIT' THEN amount
        WHEN transaction_type = 'TRANSFER' AND metadata->>'to_account' = account_id_param THEN amount
        ELSE -amount
    END), 0) INTO balance
    FROM cashflow_ledger
    WHERE account_id = account_id_param AND status = 'COMPLETED';

    RETURN balance;
END;
$$ LANGUAGE plpgsql;
