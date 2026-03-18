package services

import (
	"context"
	"fmt"

	"github.com/google/uuid"
	"internal/models"
	"internal/repositories"
)

// CashflowService handles business logic for cashflow operations
type CashflowService struct {
	repo *repositories.CashflowRepository
}

// NewCashflowService creates a new service instance
func NewCashflowService(repo *repositories.CashflowRepository) *CashflowService {
	return &CashflowService{repo: repo}
}

// CreateTransaction creates a transaction and its ledger entries
func (s *CashflowService) CreateTransaction(ctx context.Context, req *models.CreateLedgerRequest) (*models.CashflowLedger, error) {
	// Validate the transaction
	if err := s.validateTransaction(req); err != nil {
		return nil, fmt.Errorf("transaction validation failed: %w", err)
	}

	// Create the ledger entry
	entry, err := s.repo.CreateLedgerEntry(ctx, req)
	if err != nil {
		return nil, fmt.Errorf("failed to create ledger entry: %w", err)
	}

	return entry, nil
}

// TransferFunds handles transfers between accounts
func (s *CashflowService) TransferFunds(ctx context.Context, fromAccount, toAccount string, amount float64, createdBy string) ([]*models.CashflowLedger, error) {
	// Generate transaction ID for linking entries
	transactionID := uuid.New()

	// Create debit entry for source account
	debitEntry, err := s.repo.CreateLedgerEntry(ctx, &models.CreateLedgerRequest{
		TransactionID:   transactionID,
		AccountID:      fromAccount,
		Amount:        amount,
		Currency:      "USD", // Default for now
		TransactionType: models.Debit,
		Metadata:      models.JSONB{"transfer_to": toAccount, "reason": "transfer"},
		CreatedBy:     createdBy,
	})
	if err != nil {
		return nil, fmt.Errorf("failed to create debit entry: %w", err)
	}

	// Create credit entry for destination account
	creditEntry, err := s.repo.CreateLedgerEntry(ctx, &models.CreateLedgerRequest{
		TransactionID:   transactionID,
		AccountID:      toAccount,
		Amount:        amount,
		Currency:      "USD",
		TransactionType: models.Credit,
		Metadata:      models.JSONB{"transfer_from": fromAccount, "reason": "transfer"},
		CreatedBy:     createdBy,
	})
	if err != nil {
		// Handle rollback scenario - note actual rollback would require compensating transaction
		// since direct deletion is prevented by immutability
		return nil, fmt.Errorf("failed to create credit entry: %w", err)
	}

	return []*models.CashflowLedger{debitEntry, creditEntry}, nil
}

// GetAccountBalance retrieves account balance
func (s *CashflowService) GetAccountBalance(ctx context.Context, accountID string) (*models.BalanceResponse, error) {
	balance, err := s.repo.GetAccountBalance(ctx, accountID)
	if err != nil {
		return nil, fmt.Errorf("failed to retrieve balance: %w", err)
	}

	return balance, nil
}

// GetTransactionHistory retrieves transaction history for an account
func (s *CashflowService) GetTransactionHistory(ctx context.Context, accountID string, limit int, offset int) ([]*models.CashflowLedger, error) {
	filters := &models.QueryFilters{
		AccountID: &accountID,
		Limit:     limit,
		Offset:    offset,
	}

	entries, err := s.repo.QueryLedgerEntries(ctx, filters)
	if err != nil {
		return nil, fmt.Errorf("failed to retrieve transaction history: %w", err)
	}

	return entries, nil
}

// ReverseTransaction creates a reversing entry for a transaction
func (s *CashflowService) ReverseTransaction(ctx context.Context, originalID uuid.UUID, reason string, createdBy string) (*models.CashflowLedger, error) {
	// Get the original transaction
	original, err := s.repo.GetLedgerEntry(ctx, originalID)
	if err != nil {
		return nil, fmt.Errorf("failed to retrieve original transaction: %w", err)
	}

	// Create reversing entry with opposite amount
	reverseType := models.Credit
	if original.TransactionType == models.Credit {
		reverseType = models.Debit
	} else if original.TransactionType == models.Debit {
		reverseType = models.Credit
	}

	req := &models.CreateLedgerRequest{
		TransactionID:   uuid.New(),
		AccountID:      original.AccountID,
		Amount:        original.Amount,
		Currency:      original.Currency,
		TransactionType: reverseType,
		Metadata:      models.JSONB{"reversal_of": original.ID.String(), "reason": reason},
		CreatedBy:     createdBy,
	}

	reversal, err := s.repo.CreateLedgerEntry(ctx, req)
	if err != nil {
		return nil, fmt.Errorf("failed to create reversal entry: %w", err)
	}

	// Add audit event to original transaction
	auditEvent := models.AuditEvent{
		Event:     "REVERSAL",
		Timestamp: original.CreatedAt,
		User:      createdBy,
		Details:   models.JSONB{"reversal_id": reversal.ID.String(), "reason": reason},
	}

	if err := s.repo.AddAuditEvent(ctx, originalID, auditEvent); err != nil {
		// Log error but don't fail - audit event is not critical for reversal
		fmt.Printf("Warning: Failed to add audit event to original transaction %s: %v\n", originalID, err)
	}

	return reversal, nil
}

// validateTransaction validates transaction data
func (s *CashflowService) validateTransaction(req *models.CreateLedgerRequest) error {
	if req.Amount <= 0 {
		return fmt.Errorf("amount must be greater than zero")
	}

	// Add more validation rules as needed
	return nil
}
