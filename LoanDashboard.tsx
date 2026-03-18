import React, { useState, useEffect } from 'react';

interface Loan {
  id: number;
  principal: number;
  remaining_principal: number;
  status: string;
  created_at: string;
  next_payment_date?: string;
}

const LoanDashboard: React.FC = () => {
  const [loans, setLoans] = useState<Loan[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchLoans = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/loans/1');
      if (!response.ok) throw new Error('Failed to fetch loans');
      const data = await response.json();
      setLoans(data.loans || []);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLoans();
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Loan Dashboard</h2>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      {loading ? <div>Loading...</div> : (
        <div className="space-y-4">
          {loans.map(loan => (
            <div key={loan.id} className="p-4 border rounded">
              <p><strong>ID:</strong> {loan.id}</p>
              <p><strong>Amount:</strong> ${loan.remaining_principal.toFixed(2)}</p>
              <p><strong>Status:</strong> {loan.status}</p>
              <p><strong>Created:</strong> {new Date(loan.created_at).toLocaleDateString()}</p>
            </div>
          ))}
          {loans.length === 0 && <p>No loans found</p>}
        </div>
      )}
    </div>
  );
};

export default LoanDashboard;
