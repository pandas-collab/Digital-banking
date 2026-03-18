CREATE TABLE IF NOT EXISTS ledger (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type VARCHAR(50) NOT NULL,
    amount NUMERIC(24,4) NOT NULL CHECK (amount >= 0),
    from_account UUID,
    to_account UUID,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_ledger_created_at ON ledger(created_at);
