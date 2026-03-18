package models

import (
	"database/sql/driver"
	"encoding/json"
	"time"

	"github.com/google/uuid"
)

// TransactionType represents types of cashflow transactions
type TransactionType string

const (
	Credit    TransactionType = "CREDIT"
	Debit     TransactionType = "DEBIT"
	Transfer  TransactionType = "TRANSFER"
	Adjustment TransactionType = "ADJUSTMENT"
)

// TransactionStatus represents status of transactions
type TransactionStatus string

const (
	Pending   TransactionStatus = "PENDING"
	Completed TransactionStatus = "COMPLETED"
	Failed    TransactionStatus = "FAILED"
	Cancelled TransactionStatus = "CANCELLED"
)

// JSONB type for PostgreSQL JSONB fields
type JSONB map[string]interface{}

func (j JSONB) Value() (driver.Value, error) {
	return json.Marshal(j)
}

func (j *JSONB) Scan(value interface{}) error {
	if value == nil {
		*j = make(JSONB)
		return nil
	}

	bytes, ok := value.([]byte)
	if !ok {
		return nil
	}

	var result map[string]interface{}
	if err := json.Unmarshal(bytes, &result); err != nil {
		return err
	}

	*j = JSONB(result)
	return nil
}

// AuditEvent represents a single audit trail entry
type AuditEvent struct {
	Event     string          `json:"event"`
	Timestamp time.Time       `json:"timestamp"`
	User      string          `json:"user"`
	Details   JSONB           `json:"details"`
}

// CashflowLedger represents an immutable ledger entry
type CashflowLedger struct {
	ID            uuid.UUID         `json:"id" db:"id"`
	TransactionID uuid.UUID         `json:"transaction_id" db:"transaction_id"`
	AccountID     string           `json:"account_id" db:"account_id"`
	Amount        float64          `json:"amount" db:"amount"`
	Currency      string           `json:"currency" db:"currency"`
	TransactionType TransactionType  `json:"transaction_type" db:"transaction_type"`
	Status        TransactionStatus `json:"status" db:"status"`
	Metadata      JSONB            `json:"metadata" db:"metadata"`
	AuditTrail    []AuditEvent     `json:"audit_trail" db:"audit_trail"`
	ReferenceID   *string          `json:"reference_id,omitempty" db:"reference_id"`
	LedgerSequence int64           `json:"ledger_sequence" db:"ledger_sequence"`
	CreatedAt     time.Time        `json:"created_at" db:"created_at"`
	CreatedBy     string           `json:"created_by" db:"created_by"`
}

// CreateLedgerRequest represents the request payload for creating an entry
type CreateLedgerRequest struct {
	TransactionID   uuid.UUID       `json:"transaction_id" validate:"required"`
	AccountID      string          `json:"account_id" validate:"required"`
	Amount        float64         `json:"amount" validate:"required,ne=0"`
	Currency      string          `json:"currency" validate:"required,len=3"`
	TransactionType TransactionType  `json:"transaction_type" validate:"required,oneof=CREDIT DEBIT TRANSFER ADJUSTMENT"`
	ReferenceID   *string         `json:"reference_id,omitempty"`
	Metadata      JSONB           `json:"metadata"`
	CreatedBy     string          `json:"created_by" validate:"required"`
}

// QueryFilters represents filters for querying the ledger
type QueryFilters struct {
	AccountID     *string           `json:"account_id"`
	StartDate     *time.Time        `json:"start_date"`
	EndDate       *time.Time        `json:"end_date"`
	TransactionID *uuid.UUID        `json:"transaction_id"`
	Status        *TransactionStatus  `json:"status"`
	TransactionType *TransactionType  `json:"transaction_type"`
	Limit         int             `json:"limit"`
	Offset        int             `json:"offset"`
}

// BalanceResponse represents an account balance
type BalanceResponse struct {
	AccountID string  `json:"account_id"`
	Balance   float64 `json:"balance"`
	Currency  string  `json:"currency"`
}
