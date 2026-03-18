-- Test data for cash-flow ledger

-- Insert sample transactions
INSERT INTO cashflow_ledger (
    transaction_id, account_id, amount, currency,
    transaction_type, reference_id, metadata, created_by
) VALUES
    ('123e4567-e89b-12d3-a456-426614174000', 'acc_001', 1000.00, 'USD', 'CREDIT', 'ref_1001', '{"description": "Initial deposit", "source": "bank_transfer"}', 'system'),
    (uuid_generate_v4(), 'acc_001', -50.00, 'USD', 'DEBIT', 'ref_1002', '{"description": "Purchase online", "merchant": "example-store.com"}', 'user_001'),
    (uuid_generate_v4(), 'acc_002', 500.00, 'USD', 'CREDIT', 'ref_1003', '{"description": "Salary payment", "employer": "Company Inc"}', 'system'),
    (uuid_generate_v4(), 'acc_001', -200.00, 'USD', 'TRANSFER', 'ref_1004', '{"to_account": "acc_003", "description": "Transfer to savings"}', 'user_001'),
    (uuid_generate_v4(), 'acc_003', 200.00, 'USD', 'TRANSFER', 'ref_1005', '{"from_account": "acc_001", "description": "Transfer from checking"}', 'user_001');

-- Update statuses to completed
UPDATE cashflow_ledger SET status = 'COMPLETED' WHERE created_by != 'pending';

-- Query to verify data
SELECT * FROM cashflow_ledger ORDER BY created_at DESC;
SELECT * FROM cashflow_ledger_balance;
