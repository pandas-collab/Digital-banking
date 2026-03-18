import React, { useState } from 'react';
import { useLoan } from '../hooks/useLoan';

interface LoanApplyFormProps {
  accountId: number;
  onSuccess?: () => void;
}

export const LoanApplyForm: React.FC<LoanApplyFormProps> = ({ accountId, onSuccess }) => {
  const { createLoan } = useLoan();
  const [amount, setAmount] = useState('');
  const [interestRate, setInterestRate] = useState('');
  const [termMonths, setTermMonths] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await createLoan({
        amount: parseFloat(amount),
        interestRate: parseFloat(interestRate),
        termMonths: parseInt(termMonths),
      }, accountId);
      if (onSuccess) onSuccess();
    } catch (err) {
      console.error('Failed to apply for loan:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>Apply for Loan</h3>
      <div>
        <label>Amount:</label>
        <input type="number" step="0.01" value={amount} onChange={(e) => setAmount(e.target.value)} required />
      </div>
      <div>
        <label>Interest Rate (%):</label>
        <input type="number" step="0.01" value={interestRate} onChange={(e) => setInterestRate(e.target.value)} required />
      </div>
      <div>
        <label>Term (months):</label>
        <input type="number" value={termMonths} onChange={(e) => setTermMonths(e.target.value)} required />
      </div>
      <button type="submit" disabled={loading}>{loading ? 'Applying...' : 'Apply'}</button>
    </form>
  );
};
