CREATE TABLE IF NOT EXISTS transfers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    from_account UUID NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    to_account UUID NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    amount NUMERIC(15,2) NOT NULL CHECK (amount > 0),
    status VARCHAR(20) NOT NULL CHECK (status IN ('PENDING','COMPLETED','FAILED')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_transfers_from_account ON transfers(from_account);
CREATE INDEX IF NOT EXISTS idx_transfers_to_account ON transfers(to_account);
CREATE INDEX IF NOT EXISTS idx_transfers_created_at ON transfers(created_at DESC);
