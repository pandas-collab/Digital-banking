export const validateLoanAmount = (amount: number): string | null => {
  if (isNaN(amount)) return 'Must be a number';
  if (amount <= 0) return 'Must be greater than 0';
  if (amount > 1000000) return 'Cannot exceed $1,000,000';
  return null;
};

export const validateLoanTerm = (term: number): string | null => {
  if (isNaN(term)) return 'Must be a number';
  if (term <= 0) return 'Must be greater than 0';
  if (term > 360) return 'Cannot exceed 360 months';
  return null;
};
