-- account with 10k balance
INSERT INTO accounts (id, owner, balance) VALUES (1, 'Alice', 10000.00);

-- sample policy
INSERT INTO policies (account_id, coverage_type, coverage_amount, premium_monthly, status, next_premium_date)
VALUES (1, 'Health Shield', 500.00, 50.00, 'active', NOW() + INTERVAL '30 days');
