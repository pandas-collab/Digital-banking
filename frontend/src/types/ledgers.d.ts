export interface LedgerEntry {
  ledger_id: number;
  event_type: "transfer" | "loan_created" | "loan_repayment" | "policy_created" | "policy_payment";
  account_id: number;
  amount: number;
  balance_snapshot: number;
  metadata: Record<string, unknown>;
  created_at: string; // ISO8601
}
