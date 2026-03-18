# Cashflow Ledger - Immutable PostgreSQL System

This implementation provides a complete immutable cash-flow ledger system using PostgreSQL with JSONB audit fields.

## Architecture

- **Immutable Design**: Ledger entries cannot be updated or deleted
- **JSONB Audit Trail**: Complete history of all events in JSONB format
- **Transaction Linking**: All related transactions use the same transaction_id
- **Balance Views**: Real-time balance calculations using PostgreSQL functions

## Features

- Immutable ledger table with PostgreSQL triggers
- JSONB audit trail for every transaction
- Transfer support between accounts
- Transaction reversal support (via compensating entries)
- Balance calculations and transaction history
- Extensible metadata via JSONB fields

## Database Structure

### Primary Table: `cashflow_ledger`
- All entries are immutable
- JSONB metadata and audit_trail fields
- PostgreSQL triggers prevent updates/deletes
- Ledgers sequence for ordering

### Helper Functions
- `get_account_balance()`: Calculate current account balance
- Views: `cashflow_ledger_balance` - aggregated balances view

## Usage
