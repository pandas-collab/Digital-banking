package repositories

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"time"

	"github.com/google/uuid"
	"github.com/jmoiron/sqlx"
	"internal/models"
)

// CashflowRepository handles database operations for cashflow ledger
type CashflowRepository struct {
	db *sqlx.DB
}

// NewCashflowRepository creates a new repository instance
func NewCashflowRepository(db *sqlx.DB) *CashflowRepository {
	return &CashflowRepository{db: db}
}

// CreateLedgerEntry creates a new immutable ledger entry
func (r *CashflowRepository) CreateLedgerEntry(ctx context.Context, entry *models.CreateLedgerRequest) (*models.CashflowLedger, error) {
	query := `
		INSERT INTO cashflow_ledger (
			transaction_id, account_id, amount, currency,
			transaction_type, reference_id, metadata, created_by
		) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
		RETURNING *
	`

	metadataJSON, err := json.Marshal(entry.Metadata)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal metadata: %w", err)
	}

	var ledger models.CashflowLedger
	err = r.db.GetContext(ctx, &ledger, query,
		entry.TransactionID,
		entry.AccountID,
		entry.Amount,
		entry.Currency,
		entry.TransactionType,
		entry.ReferenceID,
		metadataJSON,
		entry.CreatedBy,
	)
	if err != nil {
		return nil, fmt.Errorf("database error creating ledger entry: %w", err)
	}

	// Parse audit trail
	if err := json.Unmarshal([]byte(ledger.AuditTrail.([]uint8)), &ledger.AuditTrail); err != nil {
		return nil, fmt.Errorf("failed to unmarshal audit trail: %w", err)
	}

	return &ledger, nil
}

// GetLedgerEntry retrieves a ledger entry by ID
func (r *CashflowRepository) GetLedgerEntry(ctx context.Context, id uuid.UUID) (*models.CashflowLedger, error) {
	var ledger models.CashflowLedger
	query := `
		SELECT * FROM cashflow_ledger
		WHERE id = $1 AND status != 'CANCELLED'
	`

	err := r.db.GetContext(ctx, &ledger, query, id)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, fmt.Errorf("ledger entry not found: %w", err)
		}
		return nil, fmt.Errorf("database error retrieving ledger entry: %w", err)
	}

	// Parse audit trail
	if err := json.Unmarshal([]byte(ledger.AuditTrail.([]uint8)), &ledger.AuditTrail); err != nil {
		return nil, fmt.Errorf("failed to unmarshal audit trail: %w", err)
	}

	return &ledger, nil
}

// GetAccountBalance retrieves the current balance for an account
func (r *CashflowRepository) GetAccountBalance(ctx context.Context, accountID string) (*models.BalanceResponse, error) {
	query := `
		SELECT account_id, get_account_balance($1) as balance, currency
		FROM cashflow_ledger
		WHERE account_id = $1
		LIMIT 1
	`

	var response models.BalanceResponse
	err := r.db.GetContext(ctx, &response, query, accountID)
	if err != nil {
		if err == sql.ErrNoRows {
			return &models.BalanceResponse{
				AccountID: accountID,
				Balance:   0,
				Currency:  "USD",
			}, nil
		}
		return nil, fmt.Errorf("database error retrieving balance: %w", err)
	}

	// If no rows, return zero balance
	if response.Currency == "" {
		response.Currency = "USD"
	}

	return &response, nil
}

// QueryLedgerEntries queries ledger entries with filters
func (r *CashflowRepository) QueryLedgerEntries(ctx context.Context, filters *models.QueryFilters) ([]*models.CashflowLedger, error) {
	query := `
		SELECT * FROM cashflow_ledger
		WHERE 1=1
	`

	args := []interface{}{}
	argCount := 0

	if filters.AccountID != nil {
		argCount++
		query += fmt.Sprintf(" AND account_id = $%d", argCount)
		args = append(args, *filters.AccountID)
	}

	if filters.TransactionID != nil {
		argCount++
		query += fmt.Sprintf(" AND transaction_id = $%d", argCount)
		args = append(args, *filters.TransactionID)
	}

	if filters.Status != nil {
		argCount++
		query += fmt.Sprintf(" AND status = $%d", argCount)
		args = append(args, *filters.Status)
	}

	if filters.TransactionType != nil {
		argCount++
		query += fmt.Sprintf(" AND transaction_type = $%d", argCount)
		args = append(args, *filters.TransactionType)
	}

	if filters.StartDate != nil {
		argCount++
		query += fmt.Sprintf(" AND created_at >= $%d", argCount)
		args = append(args, *filters.StartDate)
	}

	if filters.EndDate != nil {
		argCount++
		query += fmt.Sprintf(" AND created_at <= $%d", argCount)
		args = append(args, *filters.EndDate)
	}

	query += " ORDER BY created_at DESC"

	if filters.Limit > 0 {
		argCount++
		query += fmt.Sprintf(" LIMIT $%d", argCount)
		args = append(args, filters.Limit)
	} else {
		query += " LIMIT 100"
	}

	if filters.Offset > 0 {
		argCount++
		query += fmt.Sprintf(" OFFSET $%d", argCount)
		args = append(args, filters.Offset)
	}

	var entries []*models.CashflowLedger
	err := r.db.SelectContext(ctx, &entries, query, args...)
	if err != nil {
		return nil, fmt.Errorf("database error querying ledger entries: %w", err)
	}

	// Parse audit trails for each entry
	for i, entry := range entries {
		auditData, err := json.Marshal(entry.AuditTrail)
		if err != nil {
			return nil, fmt.Errorf("failed to marshal audit trail: %w", err)
		}

		var auditEvents []models.AuditEvent
		if err := json.Unmarshal(auditData, &auditEvents); err != nil {
			// Handle legacy format or empty data
			auditEvents = []models.AuditEvent{}
		}
		entries[i].AuditTrail = auditEvents
	}

	return entries, nil
}

// AddAuditEvent appends an audit event to a ledger entry (for reversals/adjustments)
func (r *CashflowRepository) AddAuditEvent(ctx context.Context, id uuid.UUID, event models.AuditEvent) error {
	eventJSON, err := json.Marshal(event)
	if err != nil {
		return fmt.Errorf("failed to marshal audit event: %w", err)
	}

	query := `
		UPDATE cashflow_ledger
		SET audit_trail = audit_trail || $1::jsonb
		WHERE id = $2
	`

	_, err = r.db.ExecContext(ctx, query, eventJSON, id)
	if err != nil {
		return fmt.Errorf("database error adding audit event: %w", err)
	}

	return nil
}
