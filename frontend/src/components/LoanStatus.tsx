import React, { useEffect, useState } from 'react';
import { useLoan } from '../hooks/useLoan';
import { LoanResponse } from '../api/loanClient';

interface LoanStatusProps {
  loanId: number;
}

export const LoanStatus: React.FC<LoanStatusProps> = ({ loanId }) => {
  const { getLoan } = useLoan();
  const [loan, setLoan] = useState<LoanResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLoan = async () => {
      try {
        const data = await getLoan(loanId);
        setLoan(data);
      } catch (err) {
        console.error('Failed to fetch loan:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchLoan();
    const interval = setInterval(fetchLoan, 10000);
    return () => clearInterval(interval);
  }, [loanId]);

  if (loading) return <div>Loading...</div>;
  if (!loan) return <div>Loan not found</div>;

  return (
    <div>
      <h3>Loan #{loan.id}</h3>
      <p>Status: {loan.status}</p>
      <p>Original Amount: ${loan.amount}</p>
      <p>Balance Due: ${loan.balanceDue}</p>
      <p>Monthly Payment: ${loan.monthlyRepayment}</p>
      {loan.nextDueDate && <p>Next Due: {new Date(loan.nextDueDate).toLocaleDateString()}</p>}
    </div>
  );
};
