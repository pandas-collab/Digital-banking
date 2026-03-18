import React, { useState } from 'react';

interface LoanFormProps {
  onSuccess?: () => void;
}

const LoanForm: React.FC<LoanFormProps> = ({ onSuccess }) => {
  const [principal, setPrincipal] = useState<string>('');
  const [term, setTerm] = useState<string>('12');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      const response = await fetch('/api/loans/apply', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          principal_amount: parseFloat(principal),
          term_months: parseInt(term)
        })
      });

      if (!response.ok) throw new Error('Failed to apply for loan');

      setSuccess(true);
      setPrincipal('');
      setTerm('12');
      if (onSuccess) onSuccess();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Apply for Loan</h2>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      {success && <div className="text-green-500 mb-4">Loan application submitted successfully!</div>}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block mb-1">Loan Amount ($)</label>
          <input
            type="number"
            step="0.01"
            value={principal}
            onChange={(e) => setPrincipal(e.target.value)}
            required
            className="w-full p-2 border rounded"
            placeholder="10000"
          />
        </div>

        <div>
          <label className="block mb-1">Term (months)</label>
          <select
            value={term}
            onChange={(e) => setTerm(e.target.value)}
            className="w-full p-2 border rounded"
          >
            <option value="6">6 months</option>
            <option value="12">12 months</option>
            <option value="24">24 months</option>
            <option value="36">36 months</option>
          </select>
        </div>

        <button
          type="submit"
          disabled={loading || !principal}
          className="w-full bg-blue-500 text-white p-2 rounded disabled:opacity-50"
        >
          {loading ? 'Processing...' : 'Apply for Loan'}
        </button>
      </form>
    </div>
  );
};

export default LoanForm;
