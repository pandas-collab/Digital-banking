export interface LoanApplication {
  amount: number;
  term: number;
  appliedAt: Date;
}

export interface ValidationResult {
  isValid: boolean;
  errors: Record<string, string>;
}
